import os
import base64
from datetime import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor
from models.image import Image
from models.search_history import SearchHistory
from models.text import Text
from config import db_init as db
import requests

UPLOAD_FOLDER = 'D:\code\RetrievalSystemBackend\pictures'  # 文件保存的文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 确保上传文件夹存在


def read_and_encode_image(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            return img_base64
    except Exception as e:
        print(f"读取图片失败: {e}")
        return None


# 文本检索服务函数
def text_search(keywords):
    try:
        # 调用大模型接口，假设接口返回包含图片路径或错误信息的字典
        response = requests.post('http://172.20.10.13:5000/searchfor/image', json={'keywords': keywords})
        response_data = response.json()
        code = response_data.get('code')

        if code == 200:
            # 请求成功，获取图片路径
            image_paths = response_data.get('message', [])
        elif code == 400:
            # 请求失败，获取错误信息
            error_message = response_data.get('error', '未知错误')
            return jsonify({'code': 400, 'message': error_message, 'data': None})
        else:
            # 其他情况，返回通用错误
            return jsonify({'code': -1, 'message': '未知错误', 'data': None})
    except Exception as e:
        print(f"调用大模型接口失败: {e}")
        return jsonify({'code': -1, 'message': '正在响应，请稍等', 'data': None})

    # 批量查询数据库，获取所有相关图片信息
    images = Image.query.filter(Image.path.in_([os.path.join(UPLOAD_FOLDER, path) for path in image_paths])).all()

    # 使用线程池并行处理图片读取和编码
    image_list = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(read_and_encode_image, image.path): image for image in images}
        for future in futures:
            image = futures[future]
            img_base64 = future.result()
            if img_base64:
                image_list.append({
                    'id': image.id,
                    'path': image.path,
                    'description': image.description,
                    'source': image.source,
                    'format': image.format,
                    'resolution': image.resolution,
                    'image_data': img_base64
                })

    image_out = [image["image_data"] for image in image_list]

    search_pictur = ','.join(image_paths)
    current_user_id = get_jwt_identity().get('user_id')
    # 创建检索历史记录
    new_history = SearchHistory(
        user_id=int(current_user_id),
        date=datetime.now(),
        search_type=0,
        search_text=keywords,
        search_pictur=search_pictur
    )
    db.session.add(new_history)
    db.session.commit()

    return jsonify({'code': 0, 'message': '检索成功', 'data': image_out})


def image_search(image_file):
    # 保存上传的文件到D盘pictures文件夹
    filename = secure_filename(image_file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(file_path)  # 将文件保存到指定路径

    # 调用大模型接口，传递文件路径
    try:
        response = requests.post(
            'http://172.20.10.13:5000/searchfor/text',
            json={'keywords': file_path}
        )
        response_data = response.json()
        content_list = response_data.get('message', [])
    except Exception as e:
        print(f"调用大模型接口失败: {e}")
        return jsonify({
            'code': -1,
            'message': '调用大模型接口失败',
            'data': None
        })

    # 批量查询数据库，减少查询次数
    texts = Text.query.filter(Text.content.in_(content_list)).all()
    found_content = {text.content for text in texts}
    text_list = [{'title': text.title, 'content': text.content, 'source': text.source} for text in texts]

    # 对于未找到的内容，添加默认值
    for content in content_list:
        if content not in found_content:
            text_list.append({'title': '无', 'content': content, 'source': '未知'})

    search_text = ', '.join(
        [f"Title: {text['title']}, Content: {text['content']}, Source: {text['source']}" for text in text_list])
    search_pictur = file_path

    new_history = SearchHistory(
        user_id=1,  # 假设用户ID为1
        date=datetime.now(),
        search_type=1,  # 图片检索
        search_text=search_text,
        search_pictur=search_pictur
    )
    db.session.add(new_history)

    try:
        db.session.commit()
    except Exception as e:
        print(f"数据库提交失败: {e}")
        db.session.rollback()
        return jsonify({
            'code': -1,
            'message': '数据库提交失败',
            'data': None
        })

    return jsonify({
        'code': 0,
        'message': '检索成功',
        'text_list': text_list
    })
