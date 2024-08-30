from models.user import User
from flask import jsonify
from config import db_init as db

def user_login(username, password):
    u = User.query.filter_by(username=username).first()
    if not u:
        return jsonify({'code': -1, "message": "User does not exist", "data": None})

    # 直接与数据库中的密码进行比对
    if u.password != password:
        return jsonify({'code': -2, "message": "Incorrect password, please try again", "data": None})

    u_dict = u.to_dict()
    return jsonify({'code': 0, "message": "Login successful", "data": u_dict})

def user_register(email, username, password):
    if User.query.filter_by(username=username).first():
        return jsonify({'code': -1, "message": "User already exists", "data": None})

    if User.query.filter_by(email=email).first():
        return jsonify({'code': -2, "message": "Email already exists", "data": None})

    # 直接使用用户提供的密码
    new_user = User(email=email, username=username, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'code': 0, "message": "User registered successfully", "data": new_user.to_dict()})
    except Exception as e:
        db.session.rollback()
        print(f"Failed to insert user registration into database: {e}")
        return jsonify({'code': -3, "message": "User registration failed, please try again", "data": None})

def user_edit(email, username, password, avatar, nickname):
    u = User.query.filter_by(username=username).first()
    if not u:
        return jsonify({'code': -1, "message": "User does not exist", "data": None})

    updated = False
    if email and u.email != email:
        u.email = email
        updated = True
    # 直接更新密码
    if password and u.password != password:
        u.password = password
        updated = True
    if avatar and u.avatar != avatar:
        u.avatar = avatar
        updated = True
    if nickname and u.nickname != nickname:
        u.nickname = nickname
        updated = True

    if not updated:
        return jsonify({'code': -100, "message": "No user information modified", "data": None})

    try:
        db.session.commit()
        return jsonify({'code': 0, "message": "User information successfully updated", "data": None})
    except Exception as e:
        db.session.rollback()
        print(f"Failed to update user information in the database: {e}")
        return jsonify({'code': -3, "message": "Update failed", "data": None})

def user_delete(username, password):
    u = User.query.filter_by(username=username).first()
    if not u:
        return jsonify({'code': -1, "message": "User does not exist", "data": None})

    # 直接与数据库中的密码进行比对
    if u.password != password:
        return jsonify({'code': -2, "message": "Incorrect password, please try again", "data": None})

    u.delete_flag = 1
    try:
        db.session.commit()
        return jsonify({'code': 0, "message": "User successfully deleted", "data": None})
    except Exception as e:
        db.session.rollback()
        print(f"Failed to delete user in the database: {e}")
        return jsonify({'code': -3, "message": "User deletion failed", "data": None})
