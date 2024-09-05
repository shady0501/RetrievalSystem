from config import app, db_init as db  # 导入 Flask 应用实例和数据库对象
from flask_login import UserMixin  # 导入 Flask-Login 的 UserMixin

# 使用应用上下文反射数据库结构
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据到 SQLAlchemy 的 metadata 对象中

# 定义用户模型类
class User(db.Model, UserMixin):
    __table__ = db.metadata.tables['user']  # 使用反射的表来定义模型

    def to_dict(self):
        """将 User 对象转换为字典格式"""
        return {
            'id': self.id,  # 用户 ID
            'username': self.username,  # 用户名
            'nickname': self.nickname,  # 昵称
            'avatar': self.avatar,  # 用户头像 URL
            'email': self.email,  # 用户电子邮件
            'permission_level': self.permission_level,  # 用户权限级别
            'balance': float(self.balance) if self.balance is not None else 0.0,  # 用户余额，转换为浮点数
            'search_condition_id': self.search_condition_id,  # 用户搜索条件 ID
            'filter_condition_id': self.filter_condition_id,  # 用户过滤条件 ID
            'delete_flag': self.delete_flag or 0,  # 用户删除标记，默认为 0
            'birthday': self.birthday,  # 用户生日
            'sex': self.sex,  # 用户性别
            'description': self.description,  # 用户个人简介
        }
