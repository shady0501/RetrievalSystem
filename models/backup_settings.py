from config import app, db_init as db  # 导入 Flask 应用实例和数据库对象

# 使用应用上下文反射数据库
with app.app_context():
    # 反射数据库元数据到 SQLAlchemy 的 metadata 对象中，以便后续定义模型类
    db.metadata.reflect(bind=db.engine)

# 定义系统备份设置模型类
class BackupSetting(db.Model):
    # 将数据库表 'backupsettings' 映射到 SQLAlchemy 模型 BackupSetting
    __table__ = db.metadata.tables['backupsettings']

    def to_dict(self):
        """
        将 BackupSetting 对象转换为字典格式

        Returns:
            dict: 包含备份设置信息的字典
        """
        return {
            'id': self.id,  # 备份设置 ID
            'admin_id': self.admin_id,  # 关联的管理员 ID
            'backup_frequency': self.backup_frequency,  # 备份频率（如每日、每周）
            'backup_path': self.backup_path,  # 备份文件的存储路径
        }
