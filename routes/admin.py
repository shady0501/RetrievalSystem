from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.admin import admin_edit_user_info, admin_delete_user, admin_get_user_info
from services.backup_record import get_record, create_backup
from services.backup_settings import get_setting, set_setting

# 创建管理员蓝图，用于处理与管理员相关的路由
admin = Blueprint('admin', __name__)

# 管理员修改用户信息路由
@admin.route('/edit_user_info', methods=['POST'])
@jwt_required()
def edit_user_info():
    data = request.form
    if not data:
        return jsonify({
            'code': -3,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    nickname = data.get('nickname')
    birthday = data.get('birthday')
    sex = data.get('sex')
    description = data.get('description')

    # 检查必填字段
    if not username:
        return jsonify({
            'code': -3,
            'message': '用户名为必填项',
            'data': None
        })

    # 调用管理员修改用户信息服务
    return admin_edit_user_info(username, password, email, nickname, birthday, sex, description)

# 管理员注销用户账号路由
@admin.route('/delete_user', methods=['POST'])
@jwt_required()
def delete_user():
    data = request.form
    if not data:
        return jsonify({
            'code': -3,
            'message': '无效输入',
            'data': None
        })
    username = data.get('username')
    # 检查必填字段
    if not username:
        return jsonify({
            'code': -3,
            'message': '用户名为必填项',
            'data': None
        })

    # 调用管理员注销用户账号服务
    return admin_delete_user(username)

# 管理员获取用户数据路由
@admin.route('/get_user_info', methods=['GET'])
@jwt_required()
def get_user_info():
    # 调用管理员获取用户数据服务
    return admin_get_user_info()

# 管理员获取备份设置路由
@admin.route('/get_setting', methods=['GET'])
@jwt_required()
def admin_get_setting():
    # 调用管理员备份设置服务
    return get_setting()

# 管理员更改备份设置路由
@admin.route('/set_setting', methods=['POST'])
@jwt_required()
def admin_set_setting():
    data = request.form
    if not data:
        return jsonify({
            'code': -3,
            'message': '无效输入',
            'data': None
        })

    backup_frequency = data.get('backup_frequency')
    backup_path = data.get('backup_path')

    # 调用管理员备份设置服务
    return set_setting(backup_frequency, backup_path)

# 管理员获取备份记录路由
@admin.route('/get_record', methods=['GET'])
@jwt_required()
def admin_get_record():
    # 调用管理员获取备份记录服务
    return get_record()

# 管理员进行备份路由
@admin.route('/create_backup', methods=['GET'])
@jwt_required()
def admin_create_backup():
    # 调用管理员进行备份服务
    return create_backup()
