from config import db_init as db

class Feedback(db.Model):
    __tablename__ = 'feedbackandsuggestion'  # 指定表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    content = db.Column(db.Text, nullable=True, comment='反馈内容')
    date = db.Column(db.DateTime, nullable=True, comment='反馈日期')
    status = db.Column(db.String(50), nullable=True, comment='状态')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'date': self.date,
            'status': self.status
        }
