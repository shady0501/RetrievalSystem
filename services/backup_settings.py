from flask_jwt_extended import get_jwt_identity
from config import db_init as db
from models.backup_settings import BackupSetting
from flask import jsonify

# 获取备份设置服务函数
def get_setting():
    try:
        # 查询备份设置表数据
        admin_id = get_jwt_identity().get('user_id')  # 获取当前用户ID
        setting = BackupSetting.query.filter_by(admin_id=admin_id).first()
        if not setting:
            return jsonify({
                'code': -1,
                'message': '该管理员无备份',
                'data': None
            })
        setting_dict = setting.to_dict()  # 将备份设置对象转换为字典
        return jsonify({
            'code': 0,
            'message': '获取备份设置成功',
            'data': setting_dict,
        })
    except Exception as e:
        print(f"获取备份记录失败: {e}")
        return jsonify({
            'code': -1,
            'message': '获取备份设置失败',
            'data': None
        })

# 更改备份设置服务函数
def set_setting(backup_frequency, backup_path):
    try:
        # 获取当前用户ID
        admin_id = get_jwt_identity().get('user_id')

        # 查询备份设置表数据
        setting = BackupSetting.query.filter_by(admin_id=admin_id).first()

        if setting:
            # 如果找到现有记录，更新设置
            setting.backup_frequency = backup_frequency
            setting.backup_path = backup_path
        else:
            # 如果未找到记录，创建新的设置
            setting = BackupSetting(
                admin_id=admin_id,
                backup_frequency=backup_frequency,
                backup_path=backup_path
            )
            db.session.add(setting)  # 添加到会话

        db.session.commit()  # 提交会话，保存更改

        return jsonify({
            'code': 0,
            'message': '更改备份设置成功',
            'data': setting.to_dict()  # 返回更新后的设置
        })

    except Exception as e:
        db.session.rollback()  # 如果出现错误，回滚事务
        print(f"更改备份记录失败: {e}")
        return jsonify({
            'code': -1,
            'message': '更改备份设置失败',
            'data': None
        })
