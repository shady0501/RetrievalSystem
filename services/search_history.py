import os
from concurrent.futures import ThreadPoolExecutor

from models.image import Image
from models.search_history import SearchHistory, SearchResult
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
            'message': '检索类型必须为整数：0 表示文本检索，1 表示图片检索',
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
            'message': '检索历史记录成功',
            'data': new_history.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        print(f"记录检索历史失败，数据库操作错误：{e}")
        return jsonify({
            'code': -1,
            'message': '记录检索历史失败',
            'data': None
        })

def record_search_result(user_id, history_id_list):
    """
       记录检索结果

       参数:
           user_id (int): 用户 ID
           history_id_list (list): 检索历史 ID 列表

       返回:
           JSON 响应: 包含记录结果的 JSON 对象
       """
    # 将数组转换为 JSON 字符串存储
    history_id = json.dumps(history_id_list) if history_id_list else '[]'

    # 创建新的检索历史对象
    new_result = SearchResult(
        user_id=user_id,
        history_id=history_id
    )

    try:
        db.session.add(new_result)  # 添加检索历史到数据库会话
        db.session.commit()  # 提交数据库会话

        return jsonify({
            'code': 0,
            'message': '检索历史记录成功',
            'data': new_result.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        print(f"记录检索历史失败，数据库操作错误：{e}")
        return jsonify({
            'code': -1,
            'message': '记录检索历史失败',
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
                'message': '检索历史记录未找到',
                'data': None
            })

        # 将检索历史记录转换为字典
        history_dict = history.to_dict()

        # 打印 search_text
        print(history_dict['search_text'])

        # 解析 search_pictur 字段，获取图片路径列表
        picture_paths = history_dict['search_pictur'].split(',') if history_dict['search_pictur'] else []

        # 批量查询数据库，获取所有相关图片信息
        images = Image.query.filter(Image.path.in_([os.path.join(UPLOAD_FOLDER, path) for path in picture_paths])).all()

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
        # 打印 image_list
        print(image_list)

        return jsonify({
            'code': 0,
            'message': '获取检索历史记录成功',
            'data': {
                'search_text': history_dict['search_text'],
                'date': history_dict['date'],
                'images': image_out
            }
        })

    except Exception as e:
        print(f"获取检索历史记录失败: {e}")
        return jsonify({
            'code': -1,
            'message': '获取检索历史记录失败',
            'data': None
        })



# 获取检索结果详情服务函数(长篇)
def get_search_results(result_id):
    """
       获取检索结果详情

       参数:
           result_id (int): 检索结果 ID

       返回:
           JSON 响应: 包含检索结果详情的 JSON 对象
       """
    try:
        # 根据 result_id 查询 SearchResult 表以获取对应的 history_id
        results = SearchResult.query.filter_by(id=result_id).all()
        if not results:
            return jsonify({
                'code': -1,
                'message': '未找到对应的检索结果',
                'data': None
            })

        # 初始化一个空的 history_id 列表
        history_ids = []

        # 解析每个结果的 history_id 字段（JSON 字符串 -> Python 列表）
        for result in results:
            try:
                # 将 JSON 字符串转换为 Python 列表
                ids = json.loads(result.history_id)
                history_ids.extend(ids)
            except json.JSONDecodeError:
                print(f"无法解析 history_id: {result.history_id}")
                continue

        # 将字符串列表转换为整数列表
        history_ids = list(map(int, history_ids))

        # 根据解析后的 history_id 查询 SearchHistory 表
        histories = SearchHistory.query.filter(SearchHistory.id.in_(history_ids)).all()
        history_list = [history.to_dict() for history in histories]

        return jsonify({
            'code': 0,
            'message': '获取检索历史记录成功',
            'data': history_list
        })
    except Exception as e:
        print(f"获取检索历史记录失败: {e}")
        return jsonify({
            'code': -1,
            'message': '获取检索历史记录失败',
            'data': None
        })