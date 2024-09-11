from datetime import datetime  # 导入 datetime 模块，用于日期处理
from models.user import User  # 导入 User 模型
from flask import jsonify  # 导入 jsonify 用于返回 JSON 响应
from config import db_init as db  # 导入数据库初始化配置


# 管理员修改用户信息函数
def admin_edit_user_info(username, password, email, nickname, birthday, sex, description):
    """
    修改用户信息

    参数:
        username (str): 用户名
        password (str): 密码
        email (str): 邮箱
        nickname (str): 昵称
        birthday (str): 生日
        sex (str): 性别
        description (str): 描述

    返回:
        JSON 响应: 包含操作结果的 JSON 对象
    """
    # 查询用户是否存在且未被删除
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist.',
            'data': None
        })

    # 处理生日日期格式
    if birthday:
        try:
            try:
                # 尝试使用第一种格式解析日期
                date_obj = datetime.strptime(birthday, '%Y-%m-%d')
            except ValueError:
                # 如果第一种格式失败，尝试使用第二种格式
                date_obj = datetime.strptime(birthday, '%a, %d %b %Y %H:%M:%S GMT')

            # 将日期对象转换为数据库支持的日期格式
            birthday = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': -3,
                'message': 'Invalid user birthday format',
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
            'message': 'User information not updated',
            'data': None
        })

    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': 'User information updated successfully',
            'data': u.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -3,
            'message': 'Update failed',
            'data': None
        })


# 管理员注销用户账号函数
def admin_delete_user(username):
    """
    注销用户账号

    参数:
        username (str): 用户名

    返回:
        JSON 响应: 包含操作结果的 JSON 对象
    """
    # 查询用户是否存在且未被删除
    u = User.query.filter_by(username=username, delete_flag=0).first()
    if not u:
        return jsonify({
            'code': -1,
            'message': 'User does not exist or has been deleted',
            'data': None
        })

    # 设置删除标记为1，表示已删除
    u.delete_flag = 1

    try:
        db.session.commit()  # 提交数据库会话
        return jsonify({
            'code': 0,
            'message': 'Account successfully deactivated',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 回滚数据库会话
        return jsonify({
            'code': -2,
            'message': 'Account deactivation failed',
            'data': None
        })


# 管理员获取用户数据函数
def admin_get_user_info():
    """
    获取所有未被删除的用户信息

    返回:
        JSON 响应: 包含操作结果的 JSON 对象
    """
    # 获取未被删除的用户信息
    users = User.query.filter_by(delete_flag=0).all()

    if not users:
        return jsonify({
            'code': 0,
            'message': 'No user data',
            'data': ""
        })

    # 将每个用户对象转换为字典，并存入列表
    user_data = [user.to_dict() for user in users]

    return jsonify({
        'code': 0,
        'message': 'Administrator successfully retrieved user data',
        'data': user_data
    })
