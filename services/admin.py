from datetime import datetime
from models.user import User
from flask import jsonify
from config import db_init as db

# 管理员修改用户信息函数
def admin_edit_user_info(username, password, email, nickname, birthday, sex, description):
    # 查询用户是否存在
    u = User.query.filter_by(username=username).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': '用户不存在',
            'data': None
        })

    if birthday:
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': -3,
                'message': '用户生日格式非法',
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
            'data': u.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        print(f"管理员更新用户信息失败，数据库操作错误：{e}")
        return jsonify({
            'code': -3,
            'message': '更新失败',
            'data': None
        })

# 管理员注销用户账号函数
def admin_delete_user(username):
    # 查询用户是否存在且未被删除
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': '用户不存在或已被删除',
            'data': None
        })

    # 设置删除标记为1，表示已删除
    u.delete_flag = 1

    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': '账号注销成功',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        print(f"注销用户账号失败，数据库操作错误：{e}")
        return jsonify({
            'code': -2,
            'message': '账号注销失败',
            'data': None
        })


# 管理员获取用户数据函数
def admin_get_user_info():
    # 获取未被删除的用户信息
    users = User.query.filter_by(delete_flag=0).all()

    if not users:
        return jsonify({
            'code': 0,
            'message': '无用户数据',
            'data': ""
        })
    # 将每个用户对象转换为字典，并存入列表
    user_data = [user.to_dict() for user in users]

    return jsonify({
        'code': 0,
        'message': '管理员获取用户数据成功',
        'data': user_data
    })

