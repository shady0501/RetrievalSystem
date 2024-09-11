from flask_jwt_extended import get_jwt_identity  # 导入 JWT 身份获取方法
from config import db_init as db  # 导入数据库初始化配置
from models.backup_settings import BackupSetting  # 导入备份设置模型
from flask import jsonify  # 导入 jsonify 用于返回 JSON 响应


# 获取备份设置服务函数
def get_setting():
    """
    获取当前管理员的备份设置

    返回:
        JSON 响应: 包含备份设置的 JSON 对象
    """
    try:
        # 获取当前管理员的用户ID
        admin_id = get_jwt_identity().get('user_id')
        # 查询备份设置表数据
        setting = BackupSetting.query.filter_by(admin_id=admin_id).first()

        # 如果没有找到备份设置
        if not setting:
            return jsonify({
                'code': -1,
                'message': 'This administrator has no backup settings.',
                'data': None
            })

        # 将备份设置对象转换为字典
        setting_dict = setting.to_dict()
        return jsonify({
            'code': 0,
            'message': 'Backup settings retrieved successfully',
            'data': setting_dict,
        })
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': 'Failed to retrieve backup settings',
            'data': None
        })


# 更改备份设置服务函数
def set_setting(backup_frequency, backup_path):
    """
    更改当前管理员的备份设置

    参数:
        backup_frequency (str): 备份频率
        backup_path (str): 备份路径

    返回:
        JSON 响应: 包含操作结果的 JSON 对象
    """
    try:
        # 获取当前管理员的用户ID
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
            'message': 'Backup settings changed successfully',
            'data': setting.to_dict()  # 返回更新后的设置
        })

    except Exception as e:
        db.session.rollback()  # 如果出现错误，回滚事务
        return jsonify({
            'code': -1,
            'message': 'Failed to change backup settings',
            'data': None
        })
