from config import app, db_init as db  # 导入 Flask 应用实例和数据库对象

# 使用应用上下文反射数据库元数据
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据

# 定义 smartQA 模型
class smartQA(db.Model):
    __table__ = db.metadata.tables['smartqa']  # 映射数据库表

    def to_dict(self):
        """将对象转换为字典格式"""
        return {
            'id': self.id,  # 智能问答ID
            'user_id': self.user_id,  # 用户ID
            'question': self.question,  # 智能问答问题
            'answer': self.answer,  # 智能问答回复
            'date': self.date  # 日期
        }
