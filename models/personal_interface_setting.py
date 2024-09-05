from config import app, db_init as db  # 导入 Flask 应用实例和数据库对象

# 使用应用上下文反射数据库元数据
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 将数据库元数据反射到 SQLAlchemy 的 metadata 对象中

# 定义 PersonalizedInterfaceSetting 模型，通过反射机制动态加载表
class PersonalizedInterfaceSetting(db.Model):
    __table__ = db.metadata.tables['personalizedinterfacesetting']  # 映射数据库表 'personalizedinterfacesetting' 到 SQLAlchemy 模型

    def to_dict(self):
        """
        将 PersonalizedInterfaceSetting 对象转换为字典格式

        Returns:
            dict: 包含个性化界面设置信息的字典
        """
        return {
            'id': self.id,  # 设置 ID
            'user_id': self.user_id,  # 用户 ID
            'theme': self.theme,  # 主题风格
            'font_style': self.font_style,  # 字体样式
            'background_image': self.background_image  # 背景图片
        }
