from models.user import User  # 导入 User 模型
from models.feedback_suggestion import Feedback  # 导入 Feedback 模型
from flask import jsonify  # 导入 jsonify 用于返回 JSON 响应
from datetime import datetime, timezone  # 导入 datetime 和 timezone 用于时间处理
from config import db_init as db  # 导入数据库初始化配置

# 用户反馈功能
def feedback_submission(username, content):
    """
    提交用户反馈

    参数:
        username (str): 用户名
        content (str): 反馈内容

    返回:
        JSON 响应: 包含反馈提交结果的 JSON 对象
    """
    # 查询用户是否存在
    u = User.query.filter_by(username=username).first()
    if u is None:
        return jsonify({
            'code': -5,
            "message": "This user does not exist",
            "data": None
        })

    user_id = u.id

    # 获取用户的所有反馈记录
    feedback_list = Feedback.query.filter_by(user_id=user_id).all()

    # 检查是否存在相同内容的反馈
    for feedback in feedback_list:
        if feedback is not None and feedback.content.strip() == content.strip():
            return jsonify({
                'code': -10,
                "message": "Duplicate submission",
                "data": None
            })

    # 创建新的反馈记录
    feedback = Feedback(
        user_id=user_id,
        content=content,
        date=datetime.now(timezone.utc),
        status="pending"  # 设置状态为 "pending"
    )

    try:
        db.session.add(feedback)
        db.session.commit()  # 提交事务，将数据写入数据库
        return jsonify({
            'code': 0,
            "message": "User feedback submitted successfully",
            "data": feedback.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 出现异常时回滚事务
        return jsonify({
            'code': -3,
            "message": "User feedback failed, please try again",
            "data": None
        })

# 用户获得反馈记录功能
def feedback_history(username):
    """
    获取用户的反馈历史记录

    参数:
        username (str): 用户名

    返回:
        JSON 响应: 包含反馈历史记录的 JSON 对象
    """
    # 查询用户是否存在
    u = User.query.filter_by(username=username).first()
    if u is None:
        return jsonify({
            'code': -5,
            "message": "This user does not exist",
            "data": None
        })

    # 获取用户的所有反馈记录
    feedback_list = Feedback.query.filter_by(user_id=u.id).all()

    # 将反馈记录转换为字典列表
    feedback_data = [feedback.to_dict() for feedback in feedback_list]
    return jsonify({
        'code': 0,
        "message": "User feedback history displayed successfully",
        "data": feedback_data
    })
