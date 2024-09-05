from datetime import timedelta
from flask_login import login_user
from flask_jwt_extended import create_access_token, get_jwt_identity
from file_download import generate_image, send_image

# 用户登录函数
def user_login(username, password):
    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': '用户不存在',
            'data': None
        })

    # 比较密码是否正确
    if u.password != password:
        return jsonify({
            'code': -2,
            'message': '密码错误，请重试',
            'data': None
        })

    u_dict = u.to_dict()  # 将用户对象转换为字典
    # 创建JWT访问令牌
    access_token = create_access_token(identity={'username': u.username, 'user_id': u.id},expires_delta=timedelta(hours=1))
    return jsonify({
        'code': 0,
        'message': '登录成功',
        'access_token': access_token,
        'data': u_dict
    })

# 用户注册函数
def user_register(email, username, nickname, password):
    # 检查用户名是否已存在
    if User.query.filter_by(username=username, delete_flag=0).first():
        return jsonify({
            'code': -1,
            'message': '该用户名已存在',
            'data': None
        })

    # 检查电子邮件是否已存在
    if User.query.filter_by(email=email, delete_flag=0).first():
        return jsonify({
            'code': -2,
            'message': '邮箱已存在',
            'data': None
        })

    # 创建新的用户对象
    new_user = User(email=email, username=username, nickname=nickname, password=password, delete_flag=0)

    try:
        db.session.add(new_user)  # 添加新用户到数据库会话
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': '用户注册成功',
            'data': new_user.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        print(f"用户注册失败，插入数据库失败：{e}, new_user: {new_user.__dict__}")
        return jsonify({
            'code': -3,
            'message': '用户注册失败，请重试',
            'data': None
        })

# 用户信息编辑函数
def user_edit(email, username, password, avatar, nickname, sex, birthday, description):
    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': '用户不存在',
            'data': None
        })

    updated = False  # 标记是否有字段更新

    # 更新用户信息字段
    if email and u.email != email:
        u.email = email
        updated = True
    if password and u.password != password:
        u.password = password
        updated = True
    if avatar and u.avatar != avatar:
        u.avatar = avatar
        updated = True
    if nickname and u.nickname != nickname:
        u.nickname = nickname
        updated = True
    if sex and u.sex != sex:
        u.sex = sex
        updated = True
    if birthday and u.birthday != birthday:
        u.birthday = birthday
        updated = True
    if description and u.description != description:
        u.description = description
        updated = True

    # 如果没有更新任何字段，返回未修改信息提示
    if not updated:
        return jsonify({
            'code': -100,
            'message': '未修改用户信息',
            'data': None
        })

    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': '用户信息更新成功',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        print(f"更新用户信息失败，数据库操作错误：{e}")
        return jsonify({
            'code': -3,
            'message': '更新失败',
            'data': None
        })

# 用户删除函数
def user_delete(username, password):
    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': '用户不存在',
            'data': None
        })

    # 比较密码是否正确
    if u.password != password:
        return jsonify({
            'code': -2,
            'message': '密码错误，请重试',
            'data': None
        })

    u.delete_flag = 1  # 标记用户为已删除
    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': '用户删除成功',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        print(f"删除用户失败，数据库操作错误：{e}")
        return jsonify({
            'code': -3,
            'message': '用户删除失败',
            'data': None
        })

# 获取用户余额函数
def get_user_balance():
    current_user_id = get_jwt_identity().get('user_id') # 获取当前用户ID
    u = User.query.filter_by(id=current_user_id, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': '用户不存在',
            'data': None
        })
    return jsonify({
        'code': 0,
        'message': '用户余额获取成功',
        'data': u.to_dict().get('balance')
    })

# 更改用户余额函数
def set_user_balance(money):
    current_user_id = get_jwt_identity().get('user_id')  # 获取当前用户ID
    u = User.query.filter_by(id=current_user_id, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': '用户不存在',
            'data': None
        })
    user_balance = u.to_dict().get('balance',0)
    if  float(user_balance) < float(money):
        return jsonify({
            'code': -9,
            'message': '用户余额不足',
            'data': None
        })
    # 扣除余额
    u.balance = user_balance - money

    try:
        # 提交更改到数据库
        db.session.commit()
        return jsonify({
            'code': 0,
            'message': '余额扣除成功',
            'data': u.to_dict().get('balance')
        })
    except Exception as e:
        # 如果发生错误，回滚更改
        db.session.rollback()
        return jsonify({
            'code': -10,
            'message': '数据库更新失败',
            'data': str(e)
        })

from flask import request, jsonify
from config import db_init as db, alipay
from models.user import User
import time
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest

# 用户充值函数
def user_charge(username, balance):
    # 检查是否获取到所有必要的参数
    if not username or not balance:
        return jsonify({
            'code': -1,
            'message': '缺少必要的参数',
            'data': None
        })

    try:
        balance = float(balance)  # 将 balance 转换为浮点数
        balance = round(balance, 2)  # 保证金额精确到小数点后两位
    except ValueError:
        return jsonify({
            'code': -1,
            'message': '无效的余额格式',
            'data': None
        })

    # 检查 balance 是否为正数
    if balance <= 0:
        return jsonify({
            'code': -2,
            'message': '充值金额必须大于零',
            'data': None
        })

    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -3,
            'message': '用户不存在',
            'data': None
        })

    # 生成唯一订单号
    out_trade_no = f"order_{u.id}_{int(time.time())}"
    print(out_trade_no)
    # 创建支付请求
    try:
        # 使用 api_alipay_trade_page_pay 方法创建订单
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=out_trade_no,  # 订单号
            total_amount=str(balance),  # 支付金额，必须是字符串格式，精确到小数点后两位
            subject="账户充值",  # 支付标题
            return_url="https://example.com/return",  # 支付成功后的回调地址
            notify_url="https://example.com/alipay/notify"  # 支付完成后的通知回调地址
        )

        # 构建支付链接
        alipay_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' + order_string

    except Exception as e:
        return jsonify({
            'code': -4,
            'message': f'生成支付订单失败：{str(e)}',
            'data': None
        })

    return jsonify({
        'code': 0,
        'message': '生成支付订单成功',
        'data': {
            'alipay_url': alipay_url
        }
    })

# 用户下载图片函数
def user_download_picture(filename, format, resolution):
    # 从请求中获取参数
    base_image_path = 'D:/code/RetrievalSystemBackend/return_image/'
    temp_image_path = 'D:/code/RetrievalSystemBackend/return_image/'

    # 调用生成图片的函数
    new_filename, new_filepath = generate_image(filename, format, resolution, base_image_path, temp_image_path)

    # 使用发送图片的函数
    return send_image(new_filepath, new_filename)

