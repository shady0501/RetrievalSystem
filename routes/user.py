from flask import Blueprint, request, jsonify # 导入 Flask Blueprint、request、jsonify、redirect 和 url_for
from flask_jwt_extended import jwt_required  # 导入 JWT 认证所需的装饰器
from services.user import (
    user_login, user_register, user_edit, user_delete,
    get_user_balance, set_user_balance, user_charge, user_download_picture, user_dialog, user_reset_password
)  # 导入用户相关服务
from services.feedback_suggestion import feedback_submission, feedback_history  # 导入反馈建议相关服务
from file_upload import handle_file_upload  # 导入文件上传处理函数
from services.personal_interface_setting import personal_setting  # 导入个人界面设置服务

# 创建用户蓝图，用于处理与用户相关的路由
user = Blueprint('user', __name__)

# 登录路由
@user.route('/login', methods=['POST'])
def login():
    """
    处理用户登录请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    username = data.get('username')
    password = data.get('password')

    # 检查必填字段
    if not username or not password:
        return jsonify({
            'code': -4,
            'message': 'Username and password are required fields',
            'data': None
        })

    # 调用用户登录服务
    return user_login(username, password)

# 注册路由
@user.route('/register', methods=['POST'])
def register():
    """
    处理用户注册请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    email = data.get('email')
    username = data.get('username')
    nickname = data.get('nickname')
    password = data.get('password')
    permission_level = data.get('permission_level')

    # 检查必填字段
    if not email or not username or not password or not nickname:
        return jsonify({
            'code': -4,
            'message': 'All fields are required',
            'data': None
        })

    # 调用用户注册服务
    return user_register(email, username, nickname, password)

# 用户重置密码路由
@user.route('/reset_password', methods=['POST'])
def reset_password():
    """
    处理用户重置密码请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    print(data)

    username = data.get('username')
    password = data.get('password')

    # 用户名是必填字段
    if not username:
        return jsonify({
            'code': -4,
            'message': 'Username is a required field',
            'data': None
        })

    # 调用用户信息编辑服务
    return user_reset_password(username, password)

# 编辑用户信息路由
@user.route('/edit', methods=['POST'])
@jwt_required()
def edit():
    """
    处理编辑用户信息请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    upload_folder = 'D:/code/RetrievalSystemBackend/avatar/'
    response = handle_file_upload(upload_folder, 'avatar')
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

    # 调用用户信息编辑服务
    return user_edit(email, password, avatar, nickname, sex, birthday, description)

# 删除用户路由
@user.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    """
    处理删除用户请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    username = data.get('username')
    password = data.get('password')

    # 检查必填字段
    if not username or not password:
        return jsonify({
            'code': -4,
            'message': 'Username and password are required fields',
            'data': None
        })

    # 调用用户删除服务
    return user_delete(username, password)

# 获取用户余额路由
@user.route('/get_user_balance', methods=['GET'])
@jwt_required()
def get_balance():
    """
    处理获取用户余额请求
    """
    return get_user_balance()

# 更改用户余额路由
@user.route('/set_user_balance', methods=['POST'])
@jwt_required()
def set_balance():
    """
    处理更改用户余额请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    money = data.get('money')
    if money is None or float(money) < 0:
        return jsonify({
            'code': -6,
            'message': 'Invalid deduction amount',
            'data': None
        })

    return set_user_balance(money)

# 用户充值路由
@user.route('/charge', methods=['POST'])
@jwt_required()
def charge():
    """
    处理用户充值请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    username = data.get('username')
    balance = data.get('balance')

    # 检查必填字段
    if not username or not balance:
        return jsonify({
            'code': -4,
            'message': 'Username and balance are required fields',
            'data': None
        })

    # 调用用户充值服务
    return user_charge(username, balance)

# 用户反馈路由
@user.route('/feedback', methods=['POST'])
@jwt_required()
def feedback():
    """
    处理用户反馈提交请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    username = data.get('username')
    content = data.get('content')
    if not username or not content:
        return jsonify({
            'code': -4,
            'message': 'Username and content are required fields',
            'data': None
        })

    return feedback_submission(username, content)

# 编辑用户个性化设置路由
@user.route('/personal', methods=['POST'])
@jwt_required()
def personal_interface_setting():
    """
    处理编辑用户个性化设置请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    upload_folder = 'D:/code/RetrievalSystemBackend/background_image/'
    response = handle_file_upload(upload_folder, 'imgUrl')
    response_data = response.get_json()
    if response_data['code'] == 0:
        background_image = response_data['data']['file_path']
    else:
        background_image = None

    theme = data.get('theme')
    font_style = data.get('font_style')

    # 调用用户信息编辑服务
    return personal_setting(theme, font_style, background_image)

# 用户对话路由
@user.route('/dialog', methods=['POST'])
@jwt_required()
def dialog():
    """
    处理用户对话请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    content = data.get('content')

    # 检查必填字段
    if not content:
        return jsonify({
            'code': -4,
            'message': 'Search text is a required field',
            'data': None
        })

    # 调用用户对话服务
    return user_dialog(content)

# 用户下载图片路由
@user.route('/download', methods=['POST'])
@jwt_required()
def download_picture():
    """
    处理用户下载图片请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    filename = data.get('filename')
    format = data.get('format')
    resolution = data.get('resolution')

    # 检查必填字段
    if not format or not resolution:
        return jsonify({
            'code': -4,
            'message': 'All fields are required',
            'data': None
        })

    # 调用用户下载图片服务
    return user_download_picture(filename, format, resolution)

# 用户获得反馈记录路由
@user.route('/get_feedback_history', methods=['POST'])
@jwt_required()
def get_feedback_history():
    """
    处理获取用户反馈记录请求
    """
    data = request.form
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    username = data.get('username')

    # 调用用户反馈历史记录服务
    return feedback_history(username)
