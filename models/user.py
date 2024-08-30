from config import app, db_init as db

# 使用应用上下文反射数据库
with app.app_context():
    db.metadata.reflect(bind=db.engine)

class User(db.Model):
    __table__ = db.metadata.tables['user']  # 使用反射的表

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'email': self.email,
            # 出于安全考虑，不建议在API中返回密码字段
            'permission_level': self.permission_level,
            'balance': float(self.balance),
            'search_condition_id': self.search_condition_id,
            'filter_condition_id': self.filter_condition_id,
            'delete_flag': self.delete_flag
        }
