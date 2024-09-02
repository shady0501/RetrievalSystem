from config import app, db_init as db

# 使用应用上下文反射数据库
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据

# 定义 SearchHistory 模型，通过反射机制动态加载表
class SearchHistory(db.Model):
    __table__ = db.metadata.tables['searchhistory']  # 使用反射的表

    def to_dict(self):
        return {
            'id': self.id,  # 检索历史ID
            'user_id': self.user_id,  # 用户ID
            'date': self.date,  # 检索时间
            'search_type': self.search_type,  # 检索类型，布尔类型：0为文本检索，1为图片检索
            'search_text': self.search_text,  # 检索文本
            'search_pictur': self.search_pictur  # 检索图片路径
        }

# 定义 SearchResult 模型，通过反射机制动态加载表
class SearchResult(db.Model):
    __table__ = db.metadata.tables['searchresult']  # 使用反射的表

    def to_dict(self):
        return {
            'id': self.id,  # 检索结果ID
            'user_id': self.user_id,
            'history_id': self.history_id,  # 检索历史ID
            'sorting_id': self.sorting_id,
            'filter_id': self.filter_id,
            'result_type': self.result_type # 结果类型
        }
