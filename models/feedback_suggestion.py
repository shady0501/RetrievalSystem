from config import app, db_init as db

# 使用应用上下文反射数据库
with app.app_context():
    db.metadata.reflect(bind=db.engine)

class Feedback(db.Model):
    __table__ = db.metadata.tables['feedbackandsuggestion']  # 指定表名

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'date': self.date,
            'status': self.status
        }
