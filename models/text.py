from config import app, db_init as db  # 导入 Flask 应用实例和数据库对象

# 使用应用上下文反射数据库元数据
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据

# 定义 Text 模型
class Text(db.Model):
    __table__ = db.metadata.tables['text']  # 映射数据库表

    def to_dict(self):
        """将对象转换为字典格式"""
        return {
            'id': self.id,  # 文本ID
            'title': self.title,  # 文本标题
            'content': self.content,  # 文本内容
            'source': self.source  # 文本来源（可选）
        }
