from flask import Blueprint, request, jsonify  # 导入 Flask Blueprint、request 和 jsonify
from flask_jwt_extended import jwt_required  # 导入 JWT 认证所需的装饰器
from services.search_history import (
    record_search_history, get_user_search_history,
)  # 导入检索历史相关服务

# 创建检索历史蓝图，用于处理与检索历史相关的路由
search_history = Blueprint('search_history', __name__)

# 记录检索历史路由 (一组对话)
@search_history.route('/record', methods=['POST'])
@jwt_required()
def record():
    """
    处理记录检索历史的请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -2,
            'message': 'Invalid input',
            'data': None
        })

    # 从请求表单中获取用户ID、检索类型、文本数组和图片路径数组
    user_id = data.get('user_id')
    search_type = data.get('search_type', type=int)  # 获取整数类型的检索类型
    search_text_list = request.form.getlist('search_text')  # 获取文本数组
    search_pictur_list = request.form.getlist('search_pictur')  # 获取图片路径数组

    # 检查必填字段
    if user_id is None or search_type is None:
        return jsonify({
            'code': -2,
            'message': 'User ID and retrieval type are required fields',
            'data': None
        })

    # 调用记录检索历史服务
    return record_search_history(user_id, search_type, search_text_list, search_pictur_list)


# 获取用户检索历史列表路由
@search_history.route('/list', methods=['POST'])
@jwt_required()
def list_history():
    """
    处理获取用户检索历史列表的请求
    """
    search_history_id = request.form.get('search_history_id', type=int)

    # 检查检索历史ID是否提供
    if search_history_id is None:
        return jsonify({
            'code': -2,
            'message': 'Retrieval history ID not provided.',
            'data': None
        })

    # 调用获取用户检索历史列表服务
    return get_user_search_history(search_history_id)

