from flask import Blueprint, request, jsonify
from services.user import user_login, user_register, user_edit, user_delete
from services.feedback_suggestion import feedback_submission

user = Blueprint('user', __name__)

@user.route('/login', methods=['POST'])
def login():
    data = request.form
    if not data:
        return jsonify({'code': -4, 'message': 'Invalid input', 'data': None})

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'code': -4, 'message': 'Username and password are required', 'data': None})

    return user_login(username, password)

@user.route('/register', methods=['POST'])
def register():
    data = request.form
    if not data:
        return jsonify({'code': -4, 'message': 'Invalid input', 'data': None})

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({'code': -4, 'message': 'All fields are required', 'data': None})

    return user_register(email, username, password)

@user.route('/edit', methods=['PUT'])
def edit():
    data = request.form
    if not data:
        return jsonify({'code': -4, 'message': 'Invalid input', 'data': None})

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    avatar = data.get('avatar')
    nickname = data.get('nickname')

    if not username:
        return jsonify({'code': -4, 'message': 'Username is required', 'data': None})

    return user_edit(email, username, password, avatar, nickname)

@user.route('/delete', methods=['DELETE'])
def delete():
    data = request.form
    if not data:
        return jsonify({'code': -4, 'message': 'Invalid input', 'data': None})

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'code': -4, 'message': 'Username and password are required', 'data': None})

    return user_delete(username, password)


@user.route('/feedback', methods=['POST'])
def feedback():
    data = request.form
    print(data)
    if not data:
        return jsonify({
            'code': -4,
            'message': 'Invalid input',
            'data': None
        })

    username = data.get('username')
    content = data.get('content')
    print("username="+username, "content="+content)
    if not username or not content:
        return jsonify({
            'code': -4,
            'message': 'All fields are required',
            'data': None
        })
    return feedback_submission(username,content)
