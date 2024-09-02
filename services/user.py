from flask_login import login_user

from file_download import generate_image, send_image
from models.user import User
from flask import jsonify
from config import db_init as db

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
    login_user(u)
    return jsonify({
        'code': 0,
        'message': '登录成功',
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
    new_user = User(email=email, username=username, nickname = nickname, password=password,delete_flag=0)

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

# 用户充值函数
def user_charge(username, balance):
    try:
        balance = float(balance)  # 将 balance 转换为浮点数
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
            'message': '余额必须大于零',
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

    u.balance += balance  # 增加用户的余额

    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': '充值成功',
            'data': u.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        print(f"更新用户余额失败，数据库操作错误：{e}")
        return jsonify({
            'code': -4,
            'message': '余额更新失败',
            'data': None
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
