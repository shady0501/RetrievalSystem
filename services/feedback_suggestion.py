from models.user import User
from datetime import datetime, timezone
from models.feedback_suggestion import Feedback
from flask import jsonify
from config import db_init as db

# 用户反馈功能
def feedback_submission(username,content):
    u = User.query.filter_by(username=username).first()
    if u is None:
        return jsonify({
            'code': -5,
            "message": "该用户不存在",
            "data": None
        })

    user_id = u.id

    # 获取用户的所有反馈记录
    feedback_list = Feedback.query.filter_by(user_id=user_id).all()

    # 遍历所有反馈记录，检查是否有内容与提交的内容相同
    for feedback in feedback_list:
        if feedback is not None and feedback.content.strip() == content.strip():
            return jsonify({
                'code': -10,
                "message": "重复提交",
                "data": None
            })

    # status说明：pending-待处理状态; in_progress-正在处理中; resolved-问题已解决; closed-不再处理
    feedback = Feedback(user_id=user_id,content=content,date=datetime.now(timezone.utc),status="pending")
    try:
        db.session.add(feedback)
        db.session.commit()  # 提交事务，将数据写入数据库
        return jsonify({
            'code': 0,
            "message": "用户反馈成功",
            "data": feedback.to_dict()
        })
    except Exception as e:
        db.session.rollback()  # 出现异常时回滚事务
        print("用户反馈数据库插入失败：" + str(e))
        return jsonify({
            'code': -3,
            "message": "用户反馈失败，请重试",
            "data": ""
        })

# 用户获得反馈记录功能
def feedback_history(username):
    u = User.query.filter_by(username=username).first()

    # 获取用户的所有反馈记录
    feedback_list = Feedback.query.filter_by(user_id=u.id).all()

    # 将反馈记录转换为字典列表
    feedback_data = [feedback.to_dict() for feedback in feedback_list]
    return jsonify({
        'code': 0,
        "message": "用户反馈历史记录显示成功",
        "data": feedback_data
    })
