from flask import Blueprint, request, jsonify  # 导入 Flask Blueprint、request 和 jsonify
from flask_jwt_extended import jwt_required  # 导入 JWT 认证所需的装饰器
from services.search import text_search, image_search  # 导入文本和图片检索服务

# 创建搜索蓝图，用于处理与搜索相关的路由
search = Blueprint('search', __name__)

# 文本检索路由
@search.route('/text', methods=['POST'])
@jwt_required()
def search_text():
    """
    处理文本检索的请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -1,
            'message': 'Invalid input',
            'data': None
        })

    keywords = data.get('keywords')

    # 检查必填字段
    if not keywords:
        return jsonify({
            'code': -4,
            'message': 'Keyword is a required field',
            'data': None
        })

    # 调用文本检索服务
    return text_search(keywords)

# 图片检索路由
@search.route('/image', methods=['POST'])
@jwt_required()
def search_image():
    """
    处理图片检索的请求
    """
    if 'image_file' not in request.files:
        return jsonify({
            'code': -4,
            'message': 'Invalid input, no image file included',
            'data': None
        })

    image_file = request.files['image_file']

    # 调用图片检索服务
    return image_search(image_file)
