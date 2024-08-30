from config import app, db_init as db

# 使用应用上下文反射数据库
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据

# 定义 Text 模型，通过反射机制动态加载表
class Text(db.Model):
    __table__ = db.metadata.tables['text']  # 使用反射的表

    def to_dict(self):
        return {
            'id': self.id,  # 文本ID
            'title': self.title,  # 文本标题
            'content': self.content,# 文本内容
            'source': self.source  # 文本来源（可选）
        }
