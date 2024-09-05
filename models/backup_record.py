from config import app, db_init as db  # 导入 Flask 应用实例和数据库对象

# 使用应用上下文反射数据库
with app.app_context():
    # 反射数据库元数据到 SQLAlchemy 的 metadata 对象中
    db.metadata.reflect(bind=db.engine)

# 定义系统备份记录模型类
class BackupRecord(db.Model):
    # 将数据库表 'backuprecord' 映射到 SQLAlchemy 模型 BackupRecord
    __table__ = db.metadata.tables['backuprecord']

    # 定义一个方法，将 BackupRecord 对象转换为字典格式，以便在 API 响应中使用
    def to_dict(self):
        """
        将 BackupRecord 对象转换为字典格式

        Returns:
            dict: 包含备份记录信息的字典
        """
        return {
            'id': self.id,  # 备份记录 ID
            'admin_id': self.admin_id,  # 关联的管理员 ID
            'backup_date': self.backup_date,  # 备份时间
            'backup_filename': self.backup_filename,  # 备份文件名
        }
