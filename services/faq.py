from models.faq import FAQ
from flask import jsonify

# 获取FAQ列表服务函数
def get_faq_list(page, per_page):
    try:
        # 查询FAQ表数据并进行分页
        faqs = FAQ.query.paginate(page=page, per_page=per_page, error_out=False)
        faq_list = [faq.to_dict() for faq in faqs.items]

        return jsonify({
            'code': '0',
            'message': '获取FAQ列表成功',
            'data': faq_list,
            'total': faqs.total,  # 总条目数
            'pages': faqs.pages,  # 总页数
            'current_page': faqs.page  # 当前页码
        })
    except Exception as e:
        print(f"获取FAQ列表失败: {e}")
        return jsonify({'code': -1, 'message': '获取FAQ列表失败', 'data': None})
