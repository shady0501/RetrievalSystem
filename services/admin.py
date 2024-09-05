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
            'message': '用户不存在',
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
