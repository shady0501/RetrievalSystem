from config import db_init as db

class PersonalizedInterfaceSetting(db.Model):
    __tablename__ = 'personalizedinterfacesetting'  # 指定表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    theme = db.Column(db.String(255), nullable=True, comment='主题')
    font_style = db.Column(db.String(255), nullable=True, comment='字体样式')
    background_image = db.Column(db.String(255), nullable=True, comment='背景图片')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'theme': self.theme,
            'font_style': self.font_style,
            'background_image': self.background_image
        }
