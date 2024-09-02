from flask import Blueprint, request, jsonify
from flask_login import login_required

from services.search_history import record_search_history, get_user_search_history, get_search_results, \
    record_search_result

# 创建检索历史蓝图，用于处理与检索历史相关的路由
search_history = Blueprint('search_history', __name__)

# 记录检索历史路由(一组对话)
@search_history.route('/record', methods=['POST'])
@login_required
def record():
    data = request.form
    if not data:
        return jsonify({
            'code': -2,
            'message': '无效输入',
            'data': None
        })

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


# 记录检索历史路由(长篇对话)
@search_history.route('/result_record', methods=['POST'])
@login_required
def result_record():
    data = request.form
    if not data:
        return jsonify({
            'code': -2,
            'message': '无效输入',
            'data': None
        })

    user_id = data.get('user_id')
    history_id_list = request.form.getlist('history_id')  # 获取文本数组

    # 检查必填字段
    if user_id is None or history_id_list is None:
        return jsonify({
            'code': -2,
            'message': '用户ID和检索类型为必填项',
            'data': None
        })

    # 调用记录检索历史服务
    return record_search_result(user_id, history_id_list)

# 获取用户检索历史列表路由
@search_history.route('/list', methods=['GET'])
@login_required
def list_history():
    user_id = request.args.get('user_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 检查用户ID是否提供
    if user_id is None:
        return jsonify({
            'code': -2,
            'message': '用户ID为必填项',
            'data': None
        })

    # 调用获取用户检索历史列表服务
    return get_user_search_history(user_id, page, per_page)

# 获取检索结果详情路由
@search_history.route('/results', methods=['GET'])
@login_required
def get_results():
    result_id = request.args.get('result_id', type=int)

    # result_id是否提供
    if result_id is None:
        return jsonify({
            'code': -2,
            'message': 'result_id为必填项',
            'data': None
        })

    # 调用获取检索结果详情服务
    return get_search_results(result_id)
