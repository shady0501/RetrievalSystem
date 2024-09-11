import os
from concurrent.futures import ThreadPoolExecutor
from models.image import Image
from models.search_history import SearchHistory
from flask import jsonify
from config import db_init as db
from datetime import datetime
import json
from services.search import UPLOAD_FOLDER, read_and_encode_image


# 记录检索历史服务函数(一组)
def record_search_history(user_id, search_type, search_text_list, search_pictur_list):
    """
        记录检索历史

        参数:
            user_id (int): 用户 ID
            search_type (int): 检索类型（0 表示文本检索，1 表示图片检索）
            search_text_list (list): 检索文本列表
            search_pictur_list (list): 检索图片列表

        返回:
            JSON 响应: 包含记录结果的 JSON 对象
        """
    # 确保 search_type 是整数 0 或 1
    if search_type not in [0, 1]:
        return jsonify({
            'code': -2,
            'message': 'Retrieval type must be an integer: 0 for text retrieval, 1 for image retrieval',
            'data': None
        })

    # 将数组转换为 JSON 字符串存储
    search_text = json.dumps(search_text_list) if search_text_list else '[]'
    search_pictur = json.dumps(search_pictur_list) if search_pictur_list else '[]'

    # 自动获取当前日期和时间
    search_date = datetime.now()

    # 创建新的检索历史对象
    new_history = SearchHistory(
        user_id=user_id,
        date=search_date,
        search_type=search_type,  # 布尔值存储，1 表示图片检索为 True
        search_text=search_text,
        search_pictur=search_pictur
    )

    try:
        db.session.add(new_history)  # 添加检索历史到数据库会话
        db.session.commit()  # 提交数据库会话

        return jsonify({
            'code': 0,
            'message': 'Retrieval history recorded successfully',
            'data': new_history.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -1,
            'message': 'Failed to record retrieval history',
            'data': None
        })


# 获取用户检索历史列表服务函数
def get_user_search_history(search_history_id):
    """
       获取用户检索历史

       参数:
           search_history_id (int): 检索历史 ID

       返回:
           JSON 响应: 包含检索历史记录的 JSON 对象
       """
    try:
        # 根据传入的search_history_id查询单个检索历史记录
        history = SearchHistory.query.filter_by(id=search_history_id).first()

        if not history:
            return jsonify({
                'code': 404,
                'message': 'Retrieval history not found',
                'data': None
            })

        # 将检索历史记录转换为字典
        history_dict = history.to_dict()

        # 解析 search_pictur 字段，获取图片路径列表
        picture_paths = history_dict['search_pictur'].split(',') if history_dict['search_pictur'] else []

        # 批量查询数据库，获取所有相关图片信息
        images = Image.query.filter(Image.path.in_([os.path.join(UPLOAD_FOLDER, path) for path in picture_paths])).all()

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

        return jsonify({
            'code': 0,
            'message': 'Retrieval history retrieved successfully',
            'data': {
                'search_text': history_dict['search_text'],
                'date': history_dict['date'],
                'images': image_out
            }
        })

    except Exception as e:
        return jsonify({
            'code': -1,
            'message': 'Failed to retrieve retrieval history',
            'data': None
        })