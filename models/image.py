from config import app, db_init as db

# 使用应用上下文反射数据库
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据

# 定义 Image 模型，通过反射机制动态加载表
class Image(db.Model):
    __table__ = db.metadata.tables['image']  # 使用反射的表

    def to_dict(self):
        return {
            'id': self.id,  # 图片ID
            'path': self.path,  # 图片路径
            'description': self.description,  # 图片描述（可选）
            'source': self.source,
            'format': self.format,
            'resolution': self.resolution
        }
