from flask import Blueprint, request, jsonify
from services.faq import get_faq_list

# 创建FAQ蓝图，用于处理与FAQ相关的路由
faq = Blueprint('faq', __name__)

# 获取FAQ列表路由
@faq.route('/get', methods=['GET'])
def get_faq():
    # 获取查询参数，默认页码为1，每页显示10条数据
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 调用获取FAQ列表服务
    return get_faq_list(page, per_page)
