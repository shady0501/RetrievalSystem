from datetime import timedelta  # 导入 timedelta 用于设置 token 过期时间
from flask import jsonify, request  # 导入 jsonify 用于返回 JSON 响应, request 用于获取请求数据
from flask_jwt_extended import create_access_token, get_jwt_identity  # 导入 JWT 相关方法
from config import db_init as db
from zhipuai import ZhipuAI # 导入ZhipuAI用于用户对话
from datetime import datetime  # 导入 datetime 用于时间处理
from models.smart_qa import smartQA # 导入 smartQA 模型
from models.user import User  # 导入 User 模型
import time  # 导入 time 用于生成订单号
from file_download import generate_image, send_image  # 导入图片生成和发送函数


# 用户登录函数
def user_login(username, password):
    """
    用户登录

    参数:
        username (str): 用户名
        password (str): 密码

    返回:
        JSON 响应: 包含登录结果和 JWT 令牌的 JSON 对象
    """
    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist',
            'data': None
        })

    # 比较密码是否正确
    if u.password != password:
        return jsonify({
            'code': -2,
            'message': 'Incorrect password, please try again',
            'data': None
        })

    u_dict = u.to_dict()  # 将用户对象转换为字典
    # 创建JWT访问令牌
    access_token = create_access_token(identity={'username': u.username, 'user_id': u.id},
                                       expires_delta=timedelta(hours=1))

    return jsonify({
        'code': 0,
        'message': 'Login successful',
        'access_token': access_token,
        'data': u_dict
    })


# 用户注册函数
def user_register(email, username, nickname, password):
    """
    用户注册

    参数:
        email (str): 用户邮箱
        username (str): 用户名
        nickname (str): 用户昵称
        password (str): 用户密码

    返回:
        JSON 响应: 包含注册结果的 JSON 对象
    """
    # 检查用户名是否已存在
    if User.query.filter_by(username=username, delete_flag=0).first():
        return jsonify({
            'code': -1,
            'message': 'This username already exists',
            'data': None
        })

    # 检查电子邮件是否已存在
    if User.query.filter_by(email=email, delete_flag=0).first():
        return jsonify({
            'code': -2,
            'message': 'Email already exists',
            'data': None
        })

    # 创建新的用户对象
    new_user = User(email=email, username=username, nickname=nickname, password=password, delete_flag=0, permission_level=1)

    try:
        db.session.add(new_user)  # 添加新用户到数据库会话
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': 'User registration successful',
            'data': new_user.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -3,
            'message': 'User registration failed, please try again',
            'data': None
        })

# 用户重置密码函数
def user_reset_password(username, password):
    """
    重置用户密码

    参数:
        username (str): 用户名
        password (str): 新的用户密码

    返回:
        JSON 响应: 包含编辑结果的 JSON 对象
    """
    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist',
            'data': None
        })

    u.password = password

    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': 'User password reset successfully',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -3,
            'message': 'Password reset failed',
            'data': None
        })


# 用户信息编辑函数
def user_edit(email, password, avatar, nickname, sex, birthday, description):
    """
    编辑用户信息

    参数:
        email (str): 新的用户邮箱
        username (str): 用户名
        password (str): 新的用户密码
        avatar (str): 新的用户头像
        nickname (str): 新的用户昵称
        sex (str): 新的用户性别
        birthday (str): 新的用户生日
        description (str): 新的用户描述

    返回:
        JSON 响应: 包含编辑结果的 JSON 对象
    """
    # 查询用户是否存在
    current_user_id = get_jwt_identity().get('user_id')  # 获取当前用户ID
    u = User.query.filter_by(id=current_user_id, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist',
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
            'message': 'User information not updated',
            'data': None
        })

    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': 'User information updated successfully',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -3,
            'message': 'Update failed',
            'data': None
        })


# 用户删除函数
def user_delete(username, password):
    """
    删除用户

    参数:
        username (str): 用户名
        password (str): 用户密码

    返回:
        JSON 响应: 包含删除结果的 JSON 对象
    """
    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist',
            'data': None
        })

    # 比较密码是否正确
    if u.password != password:
        return jsonify({
            'code': -2,
            'message': 'Incorrect password, please try again',
            'data': None
        })

    u.delete_flag = 1  # 标记用户为已删除
    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': 'User deleted successfully',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -3,
            'message': 'User deletion failed',
            'data': None
        })


# 获取用户余额函数
def get_user_balance():
    """
    获取用户余额

    返回:
        JSON 响应: 包含用户余额的 JSON 对象
    """
    current_user_id = get_jwt_identity().get('user_id')  # 获取当前用户ID
    u = User.query.filter_by(id=current_user_id, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist',
            'data': None
        })
    return jsonify({
        'code': 0,
        'message': 'User balance retrieved successfully',
        'data': u.to_dict().get('balance')
    })


# 更改用户余额函数
def set_user_balance(money):
    """
    更改用户余额

    参数:
        money (float): 要扣除的金额

    返回:
        JSON 响应: 包含更改余额结果的 JSON 对象
    """
    current_user_id = get_jwt_identity().get('user_id')  # 获取当前用户ID
    u = User.query.filter_by(id=current_user_id, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist',
            'data': None
        })
    user_balance = u.to_dict().get('balance', 0)
    if float(user_balance) < float(money):
        return jsonify({
            'code': -9,
            'message': 'Insufficient user balance',
            'data': None
        })
    # 扣除余额
    u.balance = user_balance - float(money)

    try:
        # 提交更改到数据库
        db.session.commit()
        return jsonify({
            'code': 0,
            'message': 'Balance deduction successful',
            'data': u.to_dict().get('balance')
        })
    except Exception as e:
        # 如果发生错误，回滚更改
        db.session.rollback()
        return jsonify({
            'code': -10,
            'message': 'Database update failed',
            'data': str(e)
        })


# 用户充值函数
def user_charge(username, balance):
    """
    用户充值

    参数:
        username (str): 用户名
        balance (float): 充值金额

    返回:
        JSON 响应: 包含充值结果的 JSON 对象
    """
    # 检查是否获取到所有必要的参数
    if not username or not balance:
        return jsonify({
            'code': -1,
            'message': 'Missing required parameters',
            'data': None
        })

    try:
        balance = float(balance)  # 将 balance 转换为浮点数
        balance = round(balance, 2)  # 保证金额精确到小数点后两位
    except ValueError:
        return jsonify({
            'code': -1,
            'message': 'Invalid balance format',
            'data': None
        })

    # 检查 balance 是否为正数
    if balance <= 0:
        return jsonify({
            'code': -2,
            'message': 'Recharge amount must be greater than zero',
            'data': None
        })

    # 查询用户是否存在
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -3,
            'message': 'User does not exist',
            'data': None
        })

    # 生成唯一订单号
    out_trade_no = f"order_{u.id}_{int(time.time())}"

    return jsonify({
        'code': 0,
        'message': 'Payment order generated successfully',
        'data': None
    })

# 用户对话函数
def user_dialog(content):
    client = ZhipuAI(api_key="b8700985ecb3c6e4f1a0fb5b242400a6.5IrNvh1kcywfQnYr")  # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4-0520",  # 填写需要调用的模型编码
        messages=[
            {"role": "user", "content": content},
        ],
        stream=True,
    )

    full_response = ""  # 初始化空字符串来拼接所有content
    for chunk in response:
        full_response += chunk.choices[0].delta.content  # 累加拼接content

    # 记录检索历史
    current_user_id = get_jwt_identity().get('user_id')
    new_smartQA = smartQA(
        user_id=int(current_user_id),
        question=content,
        answer=full_response,
        date=datetime.now(),
    )
    db.session.add(new_smartQA)
    db.session.commit()

    return jsonify({
        'code': 0,
        'message': full_response,
        'data': None
    })

# 用户下载图片函数
def user_download_picture(filename, format, resolution):
    """
    用户下载图片

    参数:
        filename (str): 图片文件名
        format (str): 图片格式
        resolution (str): 图片分辨率

    返回:
        图片文件: 发送图片文件作为响应
    """
    # 从请求中获取参数
    base_image_path = 'D:/code/RetrievalSystemBackend/return_image/'
    temp_image_path = 'D:/code/RetrievalSystemBackend/return_image/'

    # 调用生成图片的函数
    new_filename, new_filepath = generate_image(filename, format, resolution, base_image_path, temp_image_path)

    # 使用发送图片的函数
    return send_image(new_filepath, new_filename)
