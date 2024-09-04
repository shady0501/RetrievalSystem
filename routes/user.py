import uuid
from flask import Blueprint, request, jsonify, redirect, url_for
from alipay import Alipay
from flask_login import login_required
from services.user import user_login, user_register, user_edit, user_delete, get_user_balance, set_user_balance, user_charge, user_download_picture
from services.feedback_suggestion import feedback_submission, feedback_history
from file_upload import handle_file_upload
from flask_jwt_extended import jwt_required
from services.personal_interface_setting import personal_setting

import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse


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

# 用户重置密码路由
@user.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.form

    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    password = data.get('password')

    # 用户名是必填字段
    if not username:
        return jsonify({
            'code': -4,
            'message': '用户名为必填项',
            'data': None
        })

    # 调用用户信息编辑服务
    return user_edit(None, username, password, None, None, None, None, None)

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


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


@user.route('/pay', methods=['POST'])
# @jwt_required()
def pay():
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """

    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
    alipay_client_config.app_id = '9021000140646310'
    alipay_client_config.app_private_key = '''
    -----BEGIN RSA PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCtY0lxonfO3km2
    hI9+R5pJNYMVxLqauaTgpVG0mEwDYcwL2sdPh8o03Mt8acznmlCB8N1BtDgCerkF
    Ily4s3bXIjUi6itK753hC0b8kVxAjSIACcksppXD6uyI1n593T6xo6iNzm+jOUsR
    /6Ya05xLDoLWPBCtDeFcC7P13a7Y6ZuK0gd74ok7dcPwKfOa1ZWeoIOkd/kLseT1
    kGrNG5aIieoth1smQJwW5zMqdOLBt1XdysCQjbOF+BWQUZ1F29RfEJCQ9rsAEpeQ
    wm0Ua2D9iK6X+xUxrI4ZhWIHwQzNofYDrIUtTaYtsOR2AdvhGh0KylOMcOcMXDMf
    wJjpCK6ZAgMBAAECggEBAKsDFYo1w1NPHYcegeT8PGlelTbgPWikF8HWbJrh538i
    cz1yAEkp1j+DUlQYihgYtLUk2yWV2fRgFKLCvI8Tuu//dkdEjYSwh5hSJiawPDwS
    t2kwPbKDb4235KomXMZJdC+DCpkq9iMYPDm5W5x0AGBrJJKm1Y/J8+90P4ANsQmQ
    4b7zF9MIPeFN1y9fAe2Pu6DNnScSWAMWwS0PixXvuYlLDlX9es7px1H5V7VUBKfy
    DWldbD+BRqV2v7RKGsBhh3EXmmDvgLMQxajeaZQCCV5t5hTBfWRWocSTNIeeZ6Cu
    tdN4FHb+igJabGCQy7Po8/LUA4Y70aqavODeOFK4ks0CgYEA+fq6zUyDzpyX1wr+
    T6lwK57fDcIpCjCC1MyfpenbVsM2pEhozYJurTRYcW5rZWWH5+M0qg8oT+hLXpQU
    X+LDbJfjHrUP32Wd03/Gi8wZkv0T50K4zWiWs/X79ul8/rdv9OcxcrQKVUhqsRIm
    1PZv75ljYGsgetVDWQVYO7kDDacCgYEAsZBTNZUeLYbxYJA/5Jtncez+eruc2cnu
    2ecDCsSgIUFiXyui0kv+nTWfJHdP9Upykd/x55wmnH89rsVrWOcFYUrUs3AlaSXY
    tITd2Z0G/4J2CTp+7ym7eFepFPWMc4J8GjxVx9/MluKedu2DMOD9n/nvYtZ63gl+
    qVn7BNyYab8CgYAUc9EozuPR2boKnBmmhuRojT0OsR4OeV2a74r4ViPd+2bTFiGM
    /ujzPt8lmLUsvJvb+xjp+QeBUi4odNEd7z2x+tNYRdQgoP3CuieSdIZ7Ij2opCre
    k3oRC0UsNHpHlNaSIQBItDZMN/qStjt7HRaXceNRljI4Go7CD8/iQwbe7QKBgFiu
    2KA+ZeAfMZck9IRdCYFg+IicA27S6DR0qJRMOB3j5hnaVWvrALPMADvaS1kbYbVx
    wAQJfU9UTZ5og4DXgVxiX3FvZX/qox0l7xes0b3zjrh1OsiAc11bitso+IkIdqsz
    zzQQlsIVVUfYwFk9Re8MiX832A3leBllE3YOJyFJAoGADgAy1+h075/pSFHhscKF
    8c9J9BRdmEijrYJB44xmfVWbezRQlP6nXXDjKZyAQNCdV4TFje5mEmXgAMxUglz8
    oDvmlWR0kTds7lEgcSx1ATrkmYE5KNWwnYiqHnGsagjH8jgYSVe62JhOzqAStCFs
    CjI2QNyRZ4YCPnLP1uLf+8w=
    ...
    -----END RSA PRIVATE KEY-----
    '''

    alipay_client_config.alipay_public_key = '''
    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArWNJcaJ3zt5JtoSPfkea
    STWDFcS6mrmk4KVRtJhMA2HMC9rHT4fKNNzLfGnM55pQgfDdQbQ4Anq5BSJcuLN2
    1yI1IuorSu+d4QtG/JFcQI0iAAnJLKaVw+rsiNZ+fd0+saOojc5vozlLEf+mGtOc
    Sw6C1jwQrQ3hXAuz9d2u2OmbitIHe+KJO3XD8CnzmtWVnqCDpHf5C7Hk9ZBqzRuW
    iInqLYdbJkCcFuczKnTiwbdV3crAkI2zhfgVkFGdRdvUXxCQkPa7ABKXkMJtFGtg
    /Yiul/sVMayOGYViB8EMzaH2A6yFLU2mLbDkdgHb4RodCspTjHDnDFwzH8CY6Qiu
    mQIDAQAB
    ...
    -----END PUBLIC KEY-----
    '''

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
    """
    系统接口示例：alipay.trade.pay
    """
    # # 对照接口文档，构造请求对象
    # model = AlipayTradePayModel()
    # model.auth_code = "282877775259787048"
    # model.body = "Iphone6 16G"
    # goods_list = list()
    # goods1 = GoodsDetail()
    # goods1.goods_id = "apple-01"
    # goods1.goods_name = "ipad"
    # goods1.price = 10
    # goods1.quantity = 1
    # goods_list.append(goods1)
    # model.goods_detail = goods_list
    # model.operator_id = "yx_001"
    # model.out_trade_no = "20180510AB014"
    # model.product_code = "FACE_TO_FACE_PAYMENT"
    # model.scene = "bar_code"
    # model.store_id = ""
    # model.subject = "huabeitest"
    # model.timeout_express = "90m"
    # model.total_amount = 1
    # request = AlipayTradePayRequest(biz_model=model)
    # # 如果有auth_token、app_auth_token等其他公共参数，放在udf_params中
    # # udf_params = dict()
    # # from alipay.aop.api.constant.ParamConstants import *
    # # udf_params[P_APP_AUTH_TOKEN] = "xxxxxxx"
    # # request.udf_params = udf_params
    # # 执行请求，执行过程中如果发生异常，会抛出，请打印异常栈
    # response_content = None
    # try:
    #     response_content = client.execute(request)
    # except Exception as e:
    #     print(traceback.format_exc())
    # if not response_content:
    #     print("failed execute")
    # else:
    #     response = AlipayTradePayResponse()
    #     # 解析响应结果
    #     response.parse_response_content(response_content)
    #     print(response.body)
    #     if response.is_success():
    #         # 如果业务成功，则通过response属性获取需要的值
    #         print("get response trade_no:" + response.trade_no)
    #     else:
    #         # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
    #         print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)


    """
    带文件的系统接口示例：alipay.offline.material.image.upload
    """
    # # 如果没有找到对应Model类，则直接使用Request类，属性在Request类中
    # request = AlipayOfflineMaterialImageUploadRequest()
    # request.image_name = "我的店"
    # request.image_type = "jpg"
    # # 设置文件参数
    # f = open("/Users/foo/Downloads/IMG.jpg", "rb")
    # request.image_content = FileItem(file_name="IMG.jpg", file_content=f.read())
    # f.close()
    # response_content = None
    # try:
    #     response_content = client.execute(request)
    # except Exception as e:
    #     print(traceback.format_exc())
    # if not response_content:
    #     print("failed execute")
    # else:
    #     response = AlipayOfflineMaterialImageUploadResponse()
    #     response.parse_response_content(response_content)
    #     if response.is_success():
    #         print("get response image_url:" + response.image_url)
    #     else:
    #         print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)


    """
    页面接口示例：alipay.trade.page.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = "pay201805020000226"
    model.total_amount = 50
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    settle_detail_info = SettleDetailInfo()
    settle_detail_info.amount = 50
    settle_detail_info.trans_in_type = "userId"
    settle_detail_info.trans_in = "2088302300165604"
    settle_detail_infos = list()
    settle_detail_infos.append(settle_detail_info)
    settle_info = SettleInfo()
    settle_info.settle_detail_infos = settle_detail_infos
    model.settle_info = settle_info
    sub_merchant = SubMerchant()
    sub_merchant.merchant_id = "2088301300153242"
    model.sub_merchant = sub_merchant
    request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    response = client.page_execute(request, http_method="POST")
    print("alipay.trade.page.pay response:" + response)


    """
    构造唤起支付宝客户端支付时传递的请求串示例：alipay.trade.app.pay
    """
    model = AlipayTradeAppPayModel()
    model.timeout_express = "90m"
    model.total_amount = "9.00"
    model.seller_id = "2088301194649043"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = "Iphone6 16G"
    model.subject = "iphone"
    model.out_trade_no = "201800000001201"
    request = AlipayTradeAppPayRequest(biz_model=model)
    response = client.sdk_execute(request)
    print("alipay.trade.app.pay response:" + response)


# # 初始化支付宝SDK
# app_private_key_string = 'MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCFuWewl689rvR+ZRRRoQG2L63maR/LyRPXQ3eSpAd3BOtd70ekzoiiUgEibahHfWSWqEF5d3HdlOtl2HhpIbV+iZXm7keAu0E6vbLHYnf8sP1+S2gVOzgWVIzCRV5wKQmS0G9nDX99V5PhUK/j/VNFhJ8ndP3n2H6Uz9N8LKucMjeW1tey/4iiS9PyV3Dd5esOUD7iNgyP5ETinDIjBGJ6+bWHuNIHj1dEDjoCHIA67buHhYYJAWIGBqz773/vP5e6WywXpPfbj/Sb+om/KCUVKvPZMtWhdPLPhjqO45K3qkE/ssd80lIWL0cpfvCFItFf89DtPRJF4SnyiM9+41EnAgMBAAECggEAYwhe4SpErqLeEKkc9iMOGHWRDR13Xb1Jg1dEu4XcvWkYQhXN8iC+ka+3hV6+jEsx7l0nOCScYCREfMVmzz0Wo2KTcFWxAIYtFaqdNwoWoD4XTavcpjSYIfl10P38pYXOwDq69g/KBfKQ4wGVcXwPamGAWIFM9KGhhOWw0rpmUSLQsMwEDAAN5tPP03v0/KcninPB55xcc2PzWtPJzhWGp0Q1PyDE2bwvgYV4sas6CDTcQQ07rX2vLW9eK2eVtKOA5Q/nOv83GtdGUmtjnh2+Xc4jBdfZZ0EYx2Z2QxcOhGO3aiFKvhx3uMLfJrglE2tSVSlCixY60R6+AhmwFNxAkQKBgQDHjnwnWIQGHVBnO/c6m3ZTniUqugiSs1xnPfgyh0s2nQalKv2xXelOi0JnJ3SNaSxlY0UAQ3bT/tUTg/AqfWygx0UM7Gie6LyLXqe51xNxzvbyLUUHBer0IhgP3/C2MYqTybjM7cskKz+K85FIlfi4xBAzeXRmByxIcnMn/MYibwKBgQCrjB/c2s0Qu3rwR3FYsZysDEGcFdTU6s6Kbt8EbLRMj0kgPfr0eEtibXXB/ZxiDUt6yiOf71Go+EecvCFGXmmjxbSOlWeZIljzfgMTn6+S/bpvOVcTOpXDHVw0Ew7O2u/q6PvzvJE9zwfvbbtA51GwK6C8QlIFwIqzHI44CdY4yQKBgC3bXEReXthY3CUc7o8VMne8m6XZ4iZz+QPwhZx24p3GL8S8wFeF0RsvfS7fLjVguccCrNSGrEPDB4vYgdQBxnib0g5KNTBvIwST188o0VsRyEWWiYo3nepD+2uKdnInqESV0lWlP00scwmnNveLHwC2bVKm0kyv0UlEo5nIyG8ZAoGATvzWLvsQMQQiN0CuEAi3+wAptZTXyrHTKCqkxYTH//h50z62rpo1G70K26fKudslRgSNIrcvAn5Pevuk1qHiQmZmHMDuUrReAL+k6wQ785KgpVXhohj3nD+IlPGxf82ParqcSD4rIiqRnM0Jy3i3REbSW9ytp7hgJNihI2xkFwECgYA0uTJrl2rmP/UmnC0+PE1LyPp+tO6PGquqyK9ESWKYXbkK1er32coCBLxC7Z5m3PL2khNs5TLo1QrFiQW/7gOCGoSOQueSkIzlP+e75xFyYXctJlFt0Byk51STHj7tsXZYT991ehJndmPIX/+mREmob8HzzzB7MQJpcDZ9LK7Umw=='
# alipay_public_key_string = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhblnsJevPa70fmUUUaEBti+t5mkfy8kT10N3kqQHdwTrXe9HpM6IolIBIm2oR31klqhBeXdx3ZTrZdh4aSG1fomV5u5HgLtBOr2yx2J3/LD9fktoFTs4FlSMwkVecCkJktBvZw1/fVeT4VCv4/1TRYSfJ3T959h+lM/TfCyrnDI3ltbXsv+IokvT8ldw3eXrDlA+4jYMj+RE4pwyIwRievm1h7jSB49XRA46AhyAOu27h4WGCQFiBgas++9/7z+XulssF6T324/0m/qJvyglFSrz2TLVoXTyz4Y6juOSt6pBP7LHfNJSFi9HKX7whSLRX/PQ7T0SReEp8ojPfuNRJwIDAQAB'
# alipay = Alipay(
#     pid = "9021000140646310",  # 第3步中的APPID
#     key = alipay_public_key_string,
#     seller_id = 2088721043386745,
# )
#
# @user.route('/pay', methods=['POST'])
# def pay():
#     # 假设从前端表单接收商品信息
#     print("12356789")
#     total_amount = request.form.get('total_amount')
#     # 生成一个基于 UUID4 的订单 ID
#     order_id = str(uuid.uuid4())
#     # 构造支付参数
#     order_string = alipay.create_direct_pay_by_user_url(
#         out_trade_no=order_id,
#         total_fee=str(total_amount),
#         subject='订单描述',
#         return_url='https://localhost:8000/framework',  # 支付完成后跳转页面
#         notify_url='http://127.0.0.1:8000/user/notify'  # 异步通知地址
#     )
#     url = "https://openapi.alipaydev.com/gateway.do?" + order_string
#     return redirect(url)
#
# @user.route('/notify', methods=['POST'])
# def notify():
#     # 验证签名
#     from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
#     from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
#     from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
#     from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse
#     # 验证支付宝返回的数据签名是否正确
#     # 这里省略了详细验证过程，实际开发中需严格验证
#     # 根据返回的数据更新订单状态
#     # 假设数据库操作函数为update_order_status
#     # update_order_status(request.form['out_trade_no'], 'TRADE_SUCCESS')
#     # 必须告诉支付宝，消息已接收，防止支付宝重复发送
#     return 'success'

