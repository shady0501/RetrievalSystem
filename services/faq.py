from models.faq import FAQ  # 导入 FAQ 模型
from flask import jsonify  # 导入 jsonify 用于返回 JSON 响应

# 获取 FAQ 列表服务函数
def get_faq_list(page, per_page):
    """
    获取 FAQ 列表

    参数:
        page (int): 当前页码
        per_page (int): 每页显示的 FAQ 数量

    返回:
        JSON 响应: 包含 FAQ 列表的 JSON 对象
    """
    try:
        # 查询 FAQ 表数据并进行分页
        faqs = FAQ.query.paginate(page=page, per_page=per_page, error_out=False)
        faq_list = [faq.to_dict() for faq in faqs.items]

        return jsonify({
            'code': 0,
            'message': 'FAQ list retrieved successfully',
            'data': faq_list,
            'total': faqs.total,  # 总条目数
            'pages': faqs.pages,  # 总页数
            'current_page': faqs.page  # 当前页码
        })
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': 'Failed to retrieve FAQ list',
            'data': None
        })
