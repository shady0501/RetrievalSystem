from models.user import User
from flask import jsonify
from config import db_init as db

# 用户登录功能
def user_login(email,password):
    u = User.query.filter_by(email=email).first()
    if u is None:
        # 用户不存在
        return jsonify({
            'code': -1,
            "message": "用户不存在",
            "data": ""
        })
    u_dict = u.to_dict()
    if u_dict['password'] != password:
        # 用户存在 密码错误
        return jsonify({
            'code': -2,
            "message": "密码错误请重试",
            "data":""
        })
    return jsonify({
            'code': 0,
            "message": "登录成功",
            "data": u_dict
        })

# 用户注册功能
def user_register(email,username,password):
    u = User.query.filter_by(username=username).first()
    if u is not None:
        # 用户名已存在
        return jsonify({
            'code': -1,
            "message": "用户已存在",
            "data": ""
        })
    e = User.query.filter_by(email=email).first()
    if e is not None:
        # 邮箱已存在
        return jsonify({
            'code': -2,
            "message": "邮箱已存在",
            "data":""
        })

    new_user = User(email=email, username=username, password=password)
    u_dict = new_user.to_dict()
    try:
        db.session.add(new_user)
        db.session.commit()  # 提交事务，将数据写入数据库
        return jsonify({
            'code': 0,
            "message": "用户注册成功",
            "data": u_dict
        })
    except Exception as e:
        db.session.rollback()  # 出现异常时回滚事务
        print("用户注册数据库插入失败：" + str(e))
        return jsonify({
            'code': -3,
            "message": "用户注册失败，请重试",
            "data": ""
        })


# 用户个人信息编辑功能
def user_edit(email, username, password, avatar, nickname):
    u = User.query.filter_by(username=username).first()
    if u is None:
        # 用户不存在
        return jsonify({
            'code': -1,
            "message": "用户不存在",
            "data": ""
        })
    if (email and u.email != email) and \
            (password and u.password != password) and \
            (avatar and u.avatar != avatar) and \
            (nickname and u.nickname != nickname):
        # 用户未修改信息
        return jsonify({
            'code': -100,
            "message": "用户未修改信息",
            "data": ""
        })
    # 检查需要更新的字段
    if email:
        u.email = email
    if password:
        u.password = password
    if avatar:
        u.avatar = avatar
    if nickname:
        u.nickname = nickname

    try:
        # 提交更改到数据库
        db.session.commit()
        return jsonify({
            'code': 0,
            "message": "个人信息修改成功",
            "data": ""
        })
    except Exception as e:
        # 处理数据库提交错误
        db.session.rollback()
        print("用户个人信息编辑数据库插入失败：" + str(e))
        return jsonify({
            'code': -3,
            "message": "更新失败",
            "data": ""
        })

# 用户删除功能
def user_delete(username,password):
    u = User.query.filter_by(username=username).first()
    if u is None:
        # 用户不存在
        return jsonify({
            'code': -1,
            "message": "用户不存在",
            "data": ""
        })
    u_dict = u.to_dict()
    if u_dict['password'] != password:
        # 用户存在 密码错误
        return jsonify({
            'code': -2,
            "message": "密码错误请重试",
            "data":""
        })

    u.delete_flag = 1

    try:
        # 提交更改到数据库
        db.session.commit()
        return jsonify({
            'code': 0,
            "message": "用户删除成功",
            "data": ""
        })
    except Exception as e:
        # 处理数据库提交错误
        db.session.rollback()
        print("用户删除数据库更新失败：" + str(e))
        return jsonify({
            'code': -3,
            "message": "用户删除失败",
            "data": ""
        })



# def user_reg():
#         return jsonify({
#             'code': 200,
#             "message": "用户存在",
#             "data": ""
#         })



