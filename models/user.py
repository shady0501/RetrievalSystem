from config import db_init as db

class User(db.Model):
    __tablename__ = 'user'  # 指定表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(255), nullable=False, default='0', comment='用户名')
    nickname = db.Column(db.String(255), nullable=False, default='0', comment='用户昵称')
    avatar = db.Column(db.String(255), nullable=False, default='0', comment='头像路径')
    email = db.Column(db.String(255), nullable=False, default='0', comment='用户邮箱')
    password = db.Column(db.String(255), nullable=False, default='0', comment='用户密码')
    permission_level = db.Column(db.Integer, nullable=False, default=0, comment='权限等级')
    balance = db.Column(db.DECIMAL(10, 2), nullable=False, default=0.00, comment='账户余额')
    search_condition_id = db.Column(db.Integer, nullable=False, default=0, comment='搜索条件ID')
    filter_condition_id = db.Column(db.Integer, nullable=False, default=0, comment='过滤条件ID')
    delete_flag = db.Column(db.Integer, nullable=False, default=0, comment='过滤条件ID')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'email': self.email,
            # 出于安全考虑，不建议在API中返回密码字段
            'password': self.password,
            'permission_level': self.permission_level,
            'balance': float(self.balance),  # DECIMAL 类型转换为 float
            'search_condition_id': self.search_condition_id,
            'filter_condition_id': self.filter_condition_id,
            'delete_flag': self.delete_flag
        }