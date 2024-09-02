from config import app, db_init as db  # 导入Flask应用实例和数据库对象

# 使用应用上下文反射数据库
# 在Flask应用上下文中反射数据库结构，加载所有表的元数据
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据到SQLAlchemy的metadata对象中

# 定义搜索历史模型类
class SearchHistory(db.Model):
    # 使用反射的表来定义模型，这里直接从反射的metadata中获取表定义
    __table__ = db.metadata.tables['searchhistory']

    # 定义一个方法，将SearchHistory对象转换为字典格式，以便在API响应中使用
    def to_dict(self):
        # 返回搜索历史信息的字典表示
        return {
            'id': self.id,  # 搜索记录ID
            'user_id': self.user_id,  # 用户ID
            'date': self.date,  # 搜索日期
            'search_text': self.search_text,  # 搜索文本
            'type': self.type,  # 搜索类型
            'search_picture': self.search_picture  # 搜索图片
        }
