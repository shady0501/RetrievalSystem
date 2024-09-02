from config import app, db_init as db  # 导入Flask应用实例和数据库对象
from flask_login import UserMixin

# 使用应用上下文反射数据库
# 在Flask应用上下文中反射数据库结构，加载所有表的元数据
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据到SQLAlchemy的metadata对象中

# 定义用户模型类
class User(db.Model,UserMixin):
    # 使用反射的表来定义模型，这里直接从反射的metadata中获取表定义
    __table__ = db.metadata.tables['user']

    # 定义一个方法，将User对象转换为字典格式，以便在API响应中使用
    def to_dict(self):
        # 返回用户信息的字典表示
        return {
            'id': self.id,  # 用户ID
            'username': self.username,  # 用户名
            'nickname': self.nickname,  # 昵称
            'avatar': self.avatar,  # 用户头像URL
            'email': self.email,  # 用户电子邮件
            # 出于安全考虑，不建议在API中返回密码字段
            'permission_level': self.permission_level,  # 用户权限级别
            'balance': float(self.balance),  # 用户余额，转换为浮点数
            'search_condition_id': self.search_condition_id,  # 用户搜索条件ID
            'filter_condition_id': self.filter_condition_id,  # 用户过滤条件ID
            'delete_flag': self.delete_flag  # 用户删除标记
        }
