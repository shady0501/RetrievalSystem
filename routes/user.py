from flask import Blueprint, request
from services.user import user_login
from services.user import user_register
from services.user import user_edit
from services.user import user_delete
import json
user = Blueprint('user', __name__)

# 用户登录功能
@user.route('login', methods=['POST'])
def login():
    data = request.form
    print(request.form)
    # data = json.loads(request.data)
    # print(request.data)
    # print(request.args)
    email = data['email']
    password = data['password']

    # print(email,password)
    data = user_login(email, password)
    return data
    # return 'ok'

# 用户注册功能
@user.route('register', methods=['POST'])
def register():
    data = request.form
    print(request.form)
    email = data['email']
    username = data['username']
    password = data['password']

    # print(email,password)
    data = user_register(email, username, password)
    return data

# 用户个人信息编辑功能
@user.route('edit', methods=['PUT'])
def edit():
    data = request.form
    print(request.form)
    username = data['username']
    email = data.get('email')
    password = data.get('password')
    avatar = data.get('avatar')
    nickname = data.get('nickname')

    # print(email,password)
    data = (user_edit(email, username, password, avatar, nickname))
    return data

# 用户删除功能
@user.route('delete', methods=['DELETE'])
def delete():
    data = request.form
    print(request.form)
    username = data['username']
    password = data['password']
    data = (user_delete(username, password))
    return data



# @user.route('reg', methods=['GET'])
# def reg():
#     data = user_reg()
#     print(data)
#     return data