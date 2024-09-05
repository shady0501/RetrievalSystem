from config import app, db_init as db  # 导入 Flask 应用实例和数据库对象

# 使用应用上下文反射数据库元数据
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 将数据库元数据反射到 SQLAlchemy 的 metadata 对象中

# 定义 FAQ 模型，通过反射机制动态加载表
class FAQ(db.Model):
    __table__ = db.metadata.tables['faq']  # 将数据库表 'faq' 映射到 SQLAlchemy 模型 FAQ

    def to_dict(self):
        """
        将 FAQ 对象转换为字典格式

        Returns:
            dict: 包含 FAQ 信息的字典
        """
        return {
            'id': self.id,  # FAQ ID
            'question': self.question,  # FAQ 问题
            'answer': self.answer  # FAQ 答案
        }
