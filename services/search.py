import os

from flask_jwt_extended import get_jwt_identity

from models.image import Image
from models.search_history import SearchHistory
from models.text import Text
from werkzeug.utils import secure_filename
from config import db_init as db
import base64
from datetime import datetime
from flask import jsonify
import requests

UPLOAD_FOLDER = 'D:\code\RetrievalSystemBackend\pictures'  # 文件保存的文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 确保上传文件夹存在

# 文本检索服务函数
def text_search(keywords):
    try:
        # 调用大模型接口，假设接口返回包含图片路径或错误信息的字典
        response = requests.post('http://192.168.156.80:5000/searchfor/image', json={'keywords': keywords})
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
        return jsonify({'code': -1, 'message': '调用大模型接口失败', 'data': None})

    # 根据返回的图片路径创建模拟数据
    image_list = []
    for path in image_paths:
        # 实际查询数据库，获取图片信息
        image = Image.query.filter_by(path=UPLOAD_FOLDER+"\\"+path).first()
        if image:
            # 读取图片并转换为 Base64 编码
            try:
                with open(image.path, 'rb') as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                    image_list.append({
                        'id': image.id,
                        'path': image.path,
                        'description':image.description,
                        'source':image.source,
                        'format':image.format,
                        'resolution':image.resolution,
                        'image_data': img_base64
                    })
            except Exception as e:
                print(f"读取图片失败: {e}")
                return jsonify({'code': -1, 'message': '读取图片失败', 'data': None})

    image_out = []
    for image in image_list:
        image_out.append(image["image_data"])
    # 将查询到的图片路径转换为字符串以存储在 search_pictur
    search_pictur = ','.join(image_paths)

    current_user_id = get_jwt_identity().get('user_id')  # 获取当前用户ID
    # 创建检索历史记录
    new_history = SearchHistory(
        user_id=int(current_user_id),  # 示例用户 ID，应该替换为实际用户 ID
        date=datetime.now(),
        search_type=0,  # 文本检索
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
            'http://192.168.156.80:5000/searchfor/text',
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

    # 根据返回的内容在数据库中查询其他信息
    text_list = []
    for content in content_list:
        text = Text.query.filter_by(content=content).first()  # 根据content查询Text表
        if text:
            text_list.append({
                'title': text.title,
                'content': text.content,
                'source': text.source
            })
        else:
            text_list.append({
                'title': '无',
                'content': content,
                'source': '未知'
            })

    # 将text_list转换为字符串形式存储在数据库中
    search_text = ', '.join(
        [f"Title: {text['title']}, Content: {text['content']}, Source: {text['source']}" for text in text_list])

    search_pictur = file_path

    new_history = SearchHistory(
        user_id=1,  # 假设用户ID为1
        date=datetime.now(),
        search_type=1,  # 图片检索
        search_text=search_text,  # 使用格式化的字符串文本信息
        search_pictur=search_pictur  # 使用文件路径
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