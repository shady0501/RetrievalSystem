import os  # 导入 os 模块用于文件操作
import base64  # 导入 base64 模块用于图片编码
from datetime import datetime  # 导入 datetime 用于时间处理
from flask import jsonify  # 导入 jsonify 用于返回 JSON 响应
from flask_jwt_extended import get_jwt_identity  # 导入 get_jwt_identity 获取 JWT 用户身份
from werkzeug.utils import secure_filename  # 导入 secure_filename 用于文件名处理
from concurrent.futures import ThreadPoolExecutor  # 导入 ThreadPoolExecutor 用于并行处理
from models.image import Image  # 导入 Image 模型
from models.search_history import SearchHistory  # 导入 SearchHistory 模型
from models.text import Text  # 导入 Text 模型
from config import db_init as db  # 导入数据库配置
import requests  # 导入 requests 模块用于 HTTP 请求

# 设置图片上传文件夹路径，并确保文件夹存在
UPLOAD_FOLDER = 'D:\\code\\RetrievalSystemBackend\\pictures'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 如果文件夹不存在则创建

def read_and_encode_image(image_path):
    """
    读取图片文件并进行 Base64 编码

    参数:
        image_path (str): 图片文件路径

    返回:
        str: 图片的 Base64 编码字符串，如果读取失败则返回 None
    """
    try:
        with open(image_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            return img_base64
    except Exception as e:
        return None

# 文本检索服务函数
def text_search(keywords):
    """
    根据关键词执行文本检索

    参数:
        keywords (str): 检索关键词

    返回:
        JSON 响应: 包含检索结果的 JSON 对象
    """
    try:
        # 调用大模型接口，获取图片路径或错误信息
        response = requests.post('http://10.203.178.37:8000/searchfor/image', json={'keywords': keywords})
        response_data = response.json()
        code = response_data.get('code')

        if code == 200:
            # 请求成功，获取图片路径
            image_paths = response_data.get('message', [])
        elif code == 400:
            # 请求失败，获取错误信息
            error_message = response_data.get('error', 'Unknown error')
            return jsonify({'code': 400, 'message': error_message, 'data': None})
        else:
            # 其他情况，返回通用错误
            return jsonify({'code': -1, 'message': 'Unknown error', 'data': None})
    except Exception as e:
        return jsonify({'code': -1,
                        'message': 'Responding, please wait',
                        'data': None
                        })

    # 批量查询数据库，获取所有相关图片信息
    images = Image.query.filter(Image.path.in_([os.path.join(UPLOAD_FOLDER, path) for path in image_paths])).all()

    # 使用字典按 path 去重，确保每个图片路径只保存一次
    unique_images = list({image.path: image for image in images}.values())
    # 使用线程池并行处理图片读取和编码
    image_list = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(read_and_encode_image, image.path): image for image in unique_images}
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

    # 记录检索历史
    search_pictur = ','.join(image_paths)
    current_user_id = get_jwt_identity().get('user_id')
    new_history = SearchHistory(
        user_id=int(current_user_id),
        date=datetime.now(),
        search_type=0,
        search_text=keywords,
        search_pictur=search_pictur
    )
    db.session.add(new_history)
    db.session.commit()

    return jsonify({'code': 0,
                    'message': 'Retrieval successful',
                    'data': image_out,
                    'search_history_id': new_history.id
                    })

# 图片检索服务函数
def image_search(image_file):
    """
    根据上传的图片文件执行图片检索

    参数:
        image_file (FileStorage): 上传的图片文件对象

    返回:
        JSON 响应: 包含检索结果的 JSON 对象
    """
    # 保存上传的文件到指定文件夹
    filename = secure_filename(image_file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(file_path)  # 保存文件

    print(file_path)

    # 调用大模型接口，传递文件路径进行检索
    try:
        response = requests.post(
            'http://10.203.178.37:8000/searchfor/text',
            json={'keywords': file_path}
        )
        response_data = response.json()
        content_list = response_data.get('message', [])
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': 'Failed to call large model interface',
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

    # 记录检索历史
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
        db.session.rollback()
        return jsonify({
            'code': -1,
            'message': 'Database submission failed',
            'data': None
        })

    return jsonify({
        'code': 0,
        'message': 'Retrieval successful',
        'text_list': text_list,
        'search_history_id': new_history.id
    })
