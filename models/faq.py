from config import app, db_init as db

# 使用应用上下文反射数据库
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据

# 定义 FAQ 模型，通过反射机制动态加载表
class FAQ(db.Model):
    __table__ = db.metadata.tables['faq']  # 使用反射的表

    def to_dict(self):
        return {
            'id': self.id,  # FAQ ID
            'question': self.question,  # FAQ问题
            'answer': self.answer  # FAQ答案
        }
