from config import app, db_init as db  # 导入 Flask 应用实例和数据库对象

# 使用应用上下文反射数据库元数据
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 将数据库元数据反射到 SQLAlchemy 的 metadata 对象中

# 定义 Image 模型，通过反射机制动态加载表
class Image(db.Model):
    __table__ = db.metadata.tables['image']  # 将数据库表 'image' 映射到 SQLAlchemy 模型 Image

    def to_dict(self):
        """
        将 Image 对象转换为字典格式

        Returns:
            dict: 包含图片信息的字典
        """
        return {
            'id': self.id,  # 图片 ID
            'path': self.path,  # 图片存储路径
            'description': self.description,  # 图片描述（可选）
            'source': self.source,  # 图片来源
            'format': self.format,  # 图片格式
            'resolution': self.resolution  # 图片分辨率
        }
