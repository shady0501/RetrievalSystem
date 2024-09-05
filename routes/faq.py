from flask import Blueprint, request, jsonify  # 导入 Flask Blueprint、request 和 jsonify
from flask_jwt_extended import jwt_required  # 导入 JWT 认证所需的装饰器
from services.faq import get_faq_list  # 导入获取 FAQ 列表的服务

# 创建 FAQ 蓝图，用于处理与 FAQ 相关的路由
faq = Blueprint('faq', __name__)

# 获取 FAQ 列表路由
@faq.route('/get', methods=['GET'])
@jwt_required()
def get_faq():
    """
    处理获取 FAQ 列表的请求
    """
    # 获取查询参数，默认页码为 1，每页显示 10 条数据
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 调用获取 FAQ 列表服务
    return get_faq_list(page, per_page)
