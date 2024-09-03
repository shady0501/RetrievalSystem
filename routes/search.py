from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from services.search import text_search
from services.search import image_search

# 创建搜索蓝图，用于处理与搜索相关的路由
search = Blueprint('search', __name__)

# 文本检索路由
@search.route('/text', methods=['POST'])
@jwt_required()
def search_text():
    data = request.form
    if not data:
        return jsonify({
            'code': -1,
            'message': '无效输入',
            'data': None
        })

    keywords = data.get('keywords')

    # 检查必填字段
    if not keywords:
        return jsonify({
            'code': -4,
            'message': '关键词为必填项',
            'data': None
        })

    # 调用文本检索服务
    return text_search(keywords)

# 图片检索路由
@search.route('/image', methods=['POST'])
@jwt_required()
def search_image():
    if 'image_file' not in request.files:
        return jsonify({
            'code': -4,
            'message': '无效输入，未包含图片文件',
            'data': None
        })

    image_file = request.files['image_file']

    # 调用图片检索服务
    return image_search(image_file)