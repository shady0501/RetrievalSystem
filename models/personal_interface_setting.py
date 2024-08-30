from config import app,db_init as db

# 使用应用上下文反射数据库
with app.app_context():
    db.metadata.reflect(bind=db.engine)

class PersonalizedInterfaceSetting(db.Model):
    __table__ = db.metadata.tables['personalizedinterfacesetting']  # 使用反射的表

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'theme': self.theme,
            'font_style': self.font_style,
            'background_image': self.background_image
        }
