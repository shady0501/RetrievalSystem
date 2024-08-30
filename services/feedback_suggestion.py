from models.user import User
from datetime import datetime, timezone
from models.feedback_suggestion import Feedback
from flask import jsonify
from config import db_init as db

# 用户反馈功能
def feedback_add(id,content):
    f = Feedback.query.filter_by(id=id).first()

    f_dict = f.to_dict()
    # status说明：pending-待处理状态; in_progress-正在处理中; resolved-问题已解决; closed-不再处理
    feedback = Feedback(id=id,content=content,date=datetime.now(timezone.utc),status="pending")
    try:
        db.session.add(feedback)
        db.session.commit()  # 提交事务，将数据写入数据库
        return jsonify({
            'code': 0,
            "message": "用户反馈成功",
            "data": f_dict
        })
    except Exception as e:
        db.session.rollback()  # 出现异常时回滚事务
        print("用户注册数据库插入失败：" + str(e))
        return jsonify({
            'code': -3,
            "message": "用户注册失败，请重试",
            "data": ""
        })

