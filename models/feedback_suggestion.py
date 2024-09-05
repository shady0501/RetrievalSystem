from config import app, db_init as db  # 导入 Flask 应用实例和数据库对象

# 使用应用上下文反射数据库元数据
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 将数据库元数据反射到 SQLAlchemy 的 metadata 对象中

# 定义 Feedback 模型，通过反射机制动态加载表
class Feedback(db.Model):
    __table__ = db.metadata.tables['feedbackandsuggestion']  # 映射数据库表 'feedbackandsuggestion' 到 SQLAlchemy 模型 Feedback

    def to_dict(self):
        """
        将 Feedback 对象转换为字典格式

        Returns:
            dict: 包含反馈和建议信息的字典
        """
        return {
            'id': self.id,  # 反馈 ID
            'user_id': self.user_id,  # 用户 ID
            'content': self.content,  # 反馈内容
            'date': self.date,  # 反馈日期
            'status': self.status  # 反馈状态
        }
