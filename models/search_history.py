from config import app, db_init as db  # 导入 Flask 应用实例和数据库对象

# 使用应用上下文反射数据库元数据
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据

# 定义 SearchHistory 模型
class SearchHistory(db.Model):
    __table__ = db.metadata.tables['searchhistory']  # 映射数据库表

    def to_dict(self):
        """将对象转换为字典格式"""
        return {
            'id': self.id,  # 检索历史ID
            'user_id': self.user_id,  # 用户ID
            'date': self.date,  # 检索时间
            'search_type': self.search_type,  # 检索类型：0为文本检索，1为图片检索
            'search_text': self.search_text,  # 检索文本
            'search_pictur': self.search_pictur  # 检索图片路径
        }
