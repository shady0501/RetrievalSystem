from config import app, db_init as db  # 导入Flask应用实例和数据库对象

# 使用应用上下文反射数据库
with app.app_context():
    db.metadata.reflect(bind=db.engine)  # 反射数据库元数据到SQLAlchemy的metadata对象中

# 定义系统备份设置模型类
class BackupSetting(db.Model):
    __table__ = db.metadata.tables['backupsettings']

    # 定义一个方法，将BackupSetting对象转换为字典格式，以便在API响应中使用
    def to_dict(self):
        return {
            'id': self.id,  # 备份设置ID
            'admin_id': self.admin_id,  # 关联的管理员ID
            'backup_frequency': self.backup_frequency,  # 备份频率
            'backup_path': self.backup_path,  # 备份路径
        }
