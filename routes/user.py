from flask import Blueprint, request, jsonify
from flask_login import login_required
from services.user import user_login, user_register, user_edit, user_delete, user_charge, user_download_picture
from services.feedback_suggestion import feedback_submission, feedback_history
from file_upload import handle_file_upload
from services.personal_interface_setting import personal_setting

# 创建用户蓝图，用于处理与用户相关的路由
user = Blueprint('user', __name__)

# 登录路由
@user.route('/login', methods=['POST'])
def login():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    password = data.get('password')

    # 检查必填字段
    if not username or not password:
        return jsonify({
            'code': -4,
            'message': '用户名和密码为必填项',
            'data': None
        })

    # 调用用户登录服务
    return user_login(username, password)

# 注册路由
@user.route('/register', methods=['POST'])
def register():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    email = data.get('email')
    username = data.get('username')
    nickname = data.get('nickname')
    password = data.get('password')

    # 检查必填字段
    if not email or not username or not password or not nickname:
        return jsonify({
            'code': -4,
            'message': '所有字段均为必填项',
            'data': None
        })

    # 调用用户注册服务
    return user_register(email, username, nickname, password)

# 编辑用户信息路由
@user.route('/edit', methods=['POST'])
@login_required
def edit():
    data = request.form
    print(request.data)
    print(request.form)
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    upload_folder = 'D:/code/RetrievalSystemBackend/avatar/'
    response = handle_file_upload(upload_folder,'avatar')
    response_data = response.get_json()
    if response_data['code'] == 0:
        avatar = response_data['data']['file_path']
    else:
        avatar = None
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    nickname = data.get('nickname')
    sex = data.get('sex')
    birthday = data.get('birthday')
    description = data.get('description')

    # 用户名是必填字段
    if not username:
        return jsonify({
            'code': -4,
            'message': '用户名为必填项',
            'data': None
        })

    # 调用用户信息编辑服务
    return user_edit(email, username, password, avatar, nickname, sex, birthday, description)

# 删除用户路由
@user.route('/delete', methods=['DELETE'])
def delete():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    password = data.get('password')

    # 检查必填字段
    if not username or not password:
        return jsonify({
            'code': -4,
            'message': '用户名和密码为必填项',
            'data': None
        })

    # 调用用户删除服务
    return user_delete(username, password)

# 用户充值路由
@user.route('/charge', methods=['POST'])
def charge():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    balance = data.get('balance')

    # 检查必填字段
    if not username or not balance:
        return jsonify({
            'code': -4,
            'message': '用户名和余额为必填项',
            'data': None
        })

    # 调用用户充值服务
    return user_charge(username, balance)


@user.route('/feedback', methods=['POST'])
def feedback():
    data = request.form
    print(data)
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    content = data.get('content')
    print(username, content)
    if not username or not content:
        return jsonify({
            'code': -4,
            'message': '用户名和内容是必填项',
            'data': None
        })
    return feedback_submission(username,content)

# 编辑用户个性化设置路由
@user.route('/personal', methods=['POST'])
def personal_interface_setting():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    upload_folder = 'D:/code/RetrievalSystemBackend/background_image/'
    response = handle_file_upload(upload_folder,'background_image')
    response_data = response.get_json()
    if response_data['code'] == 0:
        background_image = response_data['data']['file_path']
    else:
        background_image = None
    username = data.get('username')
    theme = data.get('theme')
    font_style = data.get('font_style')

    # 用户名是必填字段
    if not username:
        return jsonify({
            'code': -4,
            'message': '用户名为必填项',
            'data': None
        })

    # 调用用户信息编辑服务
    return personal_setting(username,theme,font_style,background_image)

# 用户下载图片路由
@user.route('/download', methods=['POST'])
def download_picture():
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    filename = data.get('filename')
    format = data.get('format')
    resolution = data.get('resolution')

    # 检查必填字段
    if not format or not resolution:
        return jsonify({
            'code': -4,
            'message': '所有字段均为必填项',
            'data': None
        })

    # 调用用户下载图片服务
    return user_download_picture(filename, format, resolution)

# 用户获得反馈记录路由
@user.route('/get_feedback_history', methods=['POST'])
def get_feedback_history():
    data = request.form
    print(data)
    if not data:
        return jsonify({
            'code': -4,
            'message': '无效输入',
            'data': None
        })

    username = data.get('username')
    # 调用用户反馈历史记录服务
    return feedback_history(username)
