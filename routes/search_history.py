from flask import Blueprint, request, jsonify  # 导入 Flask Blueprint、request 和 jsonify
from flask_jwt_extended import jwt_required  # 导入 JWT 认证所需的装饰器
from services.search_history import (
    record_search_history, get_user_search_history,
    get_search_results, record_search_result
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
            'message': '无效输入',
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
            'message': '用户ID和检索类型为必填项',
            'data': None
        })

    # 调用记录检索历史服务
    return record_search_history(user_id, search_type, search_text_list, search_pictur_list)

# 记录检索结果路由 (长篇对话)
@search_history.route('/result_record', methods=['POST'])
@jwt_required()
def result_record():
    """
    处理记录检索结果的请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -2,
            'message': '无效输入',
            'data': None
        })

    # 从请求表单中获取用户ID和历史记录ID数组
    user_id = data.get('user_id')
    history_id_list = request.form.getlist('history_id')  # 获取历史记录ID数组

    # 检查必填字段
    if user_id is None or not history_id_list:
        return jsonify({
            'code': -2,
            'message': '用户ID和历史记录ID为必填项',
            'data': None
        })

    # 调用记录检索结果服务
    return record_search_result(user_id, history_id_list)

# 获取用户检索历史列表路由
@search_history.route('/list', methods=['GET'])
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
            'message': '未提供检索历史ID',
            'data': None
        })

    # 调用获取用户检索历史列表服务
    return get_user_search_history(search_history_id)

# 获取检索结果详情路由
@search_history.route('/results', methods=['GET'])
@jwt_required()
def get_results():
    """
    处理获取检索结果详情的请求
    """
    result_id = request.args.get('result_id', type=int)

    # 检查结果ID是否提供
    if result_id is None:
        return jsonify({
            'code': -2,
            'message': 'result_id为必填项',
            'data': None
        })

    # 调用获取检索结果详情服务
    return get_search_results(result_id)
