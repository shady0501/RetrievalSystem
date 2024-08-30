from flask import Blueprint, request, jsonify
from services.admin import admin_reset_password, admin_delete_user

# 创建管理员蓝图，用于处理与管理员相关的路由
admin = Blueprint('admin', __name__)

# 管理员重置用户密码路由
@admin.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    if not data:
        return jsonify({
            'code': -3,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    new_password = data.get('new_password')

    # 检查必填字段
    if not username or not new_password:
        return jsonify({
            'code': -3,
            'message': '用户名和新密码为必填项',
            'data': None
        })

    # 调用管理员重置用户密码服务
    return admin_reset_password(username, new_password)

# 管理员注销用户账号路由
@admin.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
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
