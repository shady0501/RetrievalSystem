from flask import Blueprint, request, jsonify, redirect
from alipay import Alipay
from flask_login import login_required
from services.user import user_login, user_register, user_edit, user_delete, get_user_balance, set_user_balance, user_charge, user_download_picture
from services.feedback_suggestion import feedback_submission, feedback_history
from file_upload import handle_file_upload
from flask_jwt_extended import jwt_required
from services.personal_interface_setting import personal_setting

# 创建用户蓝图，用于处理与用户相关的路由
user = Blueprint('user', __name__)

# 登录路由
@user.route('/login', methods=['POST'])
def login():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    password = data.get('password')

    # 检查必填字段
    if not username or not password:
        return jsonify({
            'code': -4,
            'message': '用户名和密码为必填项',
            'data': None
        })

    # 调用用户登录服务
    return user_login(username, password)

# 注册路由
@user.route('/register', methods=['POST'])
def register():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    email = data.get('email')
    username = data.get('username')
    nickname = data.get('nickname')
    password = data.get('password')

    # 检查必填字段
    if not email or not username or not password or not nickname:
        return jsonify({
            'code': -4,
            'message': '所有字段均为必填项',
            'data': None
        })

    # 调用用户注册服务
    return user_register(email, username, nickname, password)

# 编辑用户信息路由
@user.route('/edit', methods=['POST'])
@jwt_required()

def edit():
    data = request.form
    print(request.data)
    print(request.form)
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    upload_folder = 'D:/code/RetrievalSystemBackend/avatar/'
    response = handle_file_upload(upload_folder,'avatar')
    response_data = response.get_json()
    if response_data['code'] == 0:
        avatar = response_data['data']['file_path']
    else:
        avatar = None
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    nickname = data.get('nickname')
    sex = data.get('sex')
    birthday = data.get('birthday')
    description = data.get('description')

    # 用户名是必填字段
    if not username:
        return jsonify({
            'code': -4,
            'message': '用户名为必填项',
            'data': None
        })

    # 调用用户信息编辑服务
    return user_edit(email, username, password, avatar, nickname, sex, birthday, description)

# 删除用户路由
@user.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    password = data.get('password')

    # 检查必填字段
    if not username or not password:
        return jsonify({
            'code': -4,
            'message': '用户名和密码为必填项',
            'data': None
        })

    # 调用用户删除服务
    return user_delete(username, password)

# 获取用户余额路由
@user.route('/get_user_balance', methods=['GET'])
@jwt_required()
def get_balance():
    return get_user_balance()

# 更改用户余额路由
@user.route('/set_user_balance', methods=['POST'])
@jwt_required()
def set_balance():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })
    money = data.get('money')
    if money is None or float(money) < 0:
        return jsonify({
            'code': -6,
            'message': '扣款金额非法',
            'data': None
        })
    return set_user_balance(money)

# 用户充值路由
@user.route('/charge', methods=['POST'])
@jwt_required()
def charge():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    balance = data.get('balance')

    # 检查必填字段
    if not username or not balance:
        return jsonify({
            'code': -4,
            'message': '用户名和余额为必填项',
            'data': None
        })

    # 调用用户充值服务
    return user_charge(username, balance)


@user.route('/feedback', methods=['POST'])
@jwt_required()
def feedback():
    data = request.form
    print(data)
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    content = data.get('content')
    print(username, content)
    if not username or not content:
        return jsonify({
            'code': -4,
            'message': '用户名和内容是必填项',
            'data': None
        })
    return feedback_submission(username,content)

# 编辑用户个性化设置路由
@user.route('/personal', methods=['POST'])
@jwt_required()
def personal_interface_setting():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    upload_folder = 'D:/code/RetrievalSystemBackend/background_image/'
    response = handle_file_upload(upload_folder,'background_image')
    response_data = response.get_json()
    if response_data['code'] == 0:
        background_image = response_data['data']['file_path']
    else:
        background_image = None
    username = data.get('username')
    theme = data.get('theme')
    font_style = data.get('font_style')

    # 用户名是必填字段
    if not username:
        return jsonify({
            'code': -4,
            'message': '用户名为必填项',
            'data': None
        })

    # 调用用户信息编辑服务
    return personal_setting(username,theme,font_style,background_image)

# 用户下载图片路由
@user.route('/download', methods=['POST'])
@jwt_required()
def download_picture():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    filename = data.get('filename')
    format = data.get('format')
    resolution = data.get('resolution')

    # 检查必填字段
    if not format or not resolution:
        return jsonify({
            'code': -4,
            'message': '所有字段均为必填项',
            'data': None
        })

    # 调用用户下载图片服务
    return user_download_picture(filename, format, resolution)

# 用户获得反馈记录路由
@user.route('/get_feedback_history', methods=['POST'])
@jwt_required()
def get_feedback_history():
    data = request.form
    print(data)
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    # 调用用户反馈历史记录服务
    return feedback_history(username)



# 初始化支付宝SDK
# app_private_key_string = 'MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCFuWewl689rvR+ZRRRoQG2L63maR/LyRPXQ3eSpAd3BOtd70ekzoiiUgEibahHfWSWqEF5d3HdlOtl2HhpIbV+iZXm7keAu0E6vbLHYnf8sP1+S2gVOzgWVIzCRV5wKQmS0G9nDX99V5PhUK/j/VNFhJ8ndP3n2H6Uz9N8LKucMjeW1tey/4iiS9PyV3Dd5esOUD7iNgyP5ETinDIjBGJ6+bWHuNIHj1dEDjoCHIA67buHhYYJAWIGBqz773/vP5e6WywXpPfbj/Sb+om/KCUVKvPZMtWhdPLPhjqO45K3qkE/ssd80lIWL0cpfvCFItFf89DtPRJF4SnyiM9+41EnAgMBAAECggEAYwhe4SpErqLeEKkc9iMOGHWRDR13Xb1Jg1dEu4XcvWkYQhXN8iC+ka+3hV6+jEsx7l0nOCScYCREfMVmzz0Wo2KTcFWxAIYtFaqdNwoWoD4XTavcpjSYIfl10P38pYXOwDq69g/KBfKQ4wGVcXwPamGAWIFM9KGhhOWw0rpmUSLQsMwEDAAN5tPP03v0/KcninPB55xcc2PzWtPJzhWGp0Q1PyDE2bwvgYV4sas6CDTcQQ07rX2vLW9eK2eVtKOA5Q/nOv83GtdGUmtjnh2+Xc4jBdfZZ0EYx2Z2QxcOhGO3aiFKvhx3uMLfJrglE2tSVSlCixY60R6+AhmwFNxAkQKBgQDHjnwnWIQGHVBnO/c6m3ZTniUqugiSs1xnPfgyh0s2nQalKv2xXelOi0JnJ3SNaSxlY0UAQ3bT/tUTg/AqfWygx0UM7Gie6LyLXqe51xNxzvbyLUUHBer0IhgP3/C2MYqTybjM7cskKz+K85FIlfi4xBAzeXRmByxIcnMn/MYibwKBgQCrjB/c2s0Qu3rwR3FYsZysDEGcFdTU6s6Kbt8EbLRMj0kgPfr0eEtibXXB/ZxiDUt6yiOf71Go+EecvCFGXmmjxbSOlWeZIljzfgMTn6+S/bpvOVcTOpXDHVw0Ew7O2u/q6PvzvJE9zwfvbbtA51GwK6C8QlIFwIqzHI44CdY4yQKBgC3bXEReXthY3CUc7o8VMne8m6XZ4iZz+QPwhZx24p3GL8S8wFeF0RsvfS7fLjVguccCrNSGrEPDB4vYgdQBxnib0g5KNTBvIwST188o0VsRyEWWiYo3nepD+2uKdnInqESV0lWlP00scwmnNveLHwC2bVKm0kyv0UlEo5nIyG8ZAoGATvzWLvsQMQQiN0CuEAi3+wAptZTXyrHTKCqkxYTH//h50z62rpo1G70K26fKudslRgSNIrcvAn5Pevuk1qHiQmZmHMDuUrReAL+k6wQ785KgpVXhohj3nD+IlPGxf82ParqcSD4rIiqRnM0Jy3i3REbSW9ytp7hgJNihI2xkFwECgYA0uTJrl2rmP/UmnC0+PE1LyPp+tO6PGquqyK9ESWKYXbkK1er32coCBLxC7Z5m3PL2khNs5TLo1QrFiQW/7gOCGoSOQueSkIzlP+e75xFyYXctJlFt0Byk51STHj7tsXZYT991ehJndmPIX/+mREmob8HzzzB7MQJpcDZ9LK7Umw=='
# alipay_public_key_string = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhblnsJevPa70fmUUUaEBti+t5mkfy8kT10N3kqQHdwTrXe9HpM6IolIBIm2oR31klqhBeXdx3ZTrZdh4aSG1fomV5u5HgLtBOr2yx2J3/LD9fktoFTs4FlSMwkVecCkJktBvZw1/fVeT4VCv4/1TRYSfJ3T959h+lM/TfCyrnDI3ltbXsv+IokvT8ldw3eXrDlA+4jYMj+RE4pwyIwRievm1h7jSB49XRA46AhyAOu27h4WGCQFiBgas++9/7z+XulssF6T324/0m/qJvyglFSrz2TLVoXTyz4Y6juOSt6pBP7LHfNJSFi9HKX7whSLRX/PQ7T0SReEp8ojPfuNRJwIDAQAB'
# alipay = Alipay(
#     pid="9021000140646310",  # 第3步中的APPID
#     key= alipay_public_key_string,
# )

@user.route('/pay', methods=['POST'])
def pay():
    # 假设从前端表单接收商品信息
    order_id = request.form.get('order_id')
    total_amount = request.form.get('total_amount')
    # 构造支付参数
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(total_amount),
        subject='订单描述',
        return_url='https://localhost:8000/framework',  # 支付完成后跳转页面
        notify_url='https://yourdomain.com/notify'  # 异步通知地址
    )
    url = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return redirect(url)

@user.route('/notify', methods=['POST'])
def notify():
    # 验证签名
    from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
    from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
    from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
    from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse
    # 验证支付宝返回的数据签名是否正确
    # 这里省略了详细验证过程，实际开发中需严格验证
    # 根据返回的数据更新订单状态
    # 假设数据库操作函数为update_order_status
    # update_order_status(request.form['out_trade_no'], 'TRADE_SUCCESS')
    # 必须告诉支付宝，消息已接收，防止支付宝重复发送
    return 'success'