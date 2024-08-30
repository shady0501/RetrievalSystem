from models.user import User
from flask import jsonify
from config import db_init as db

# 管理员重置用户密码函数
def admin_reset_password(username, new_password):
    # 查询用户是否存在
    u = User.query.filter_by(username=username).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': '用户不存在',
            'data': None
        })

    # 重置用户密码
    u.password = new_password

    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': '密码重置成功',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        print(f"重置用户密码失败，数据库操作错误：{e}")
        return jsonify({
            'code': -2,
            'message': '密码重置失败',
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
