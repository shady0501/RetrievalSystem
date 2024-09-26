from flask_jwt_extended import get_jwt_identity  # 导入 JWT 身份获取方法
from models.backup_record import BackupRecord  # 导入备份记录模型
from models.backup_settings import BackupSetting  # 导入备份设置模型
from models.user import User  # 导入用户模型
from config import db_init as db  # 导入数据库初始化配置
from flask import jsonify  # 导入 jsonify 用于返回 JSON 响应
import os  # 导入 os 模块用于文件操作
import datetime  # 导入 datetime 模块用于日期操作
import subprocess  # 导入 subprocess 模块用于执行系统命令

# 获取备份记录服务函数
def get_record(page=1, per_page=100):
    """
    获取备份记录

    参数:
        page (int): 页码，默认为 1
        per_page (int): 每页记录数，默认为 100

    返回:
        JSON 响应: 包含备份记录的 JSON 对象
    """
    try:
        # 获取当前管理员身份
        admin_id = get_jwt_identity().get('user_id')
        admin_name = User.query.get(admin_id).username

        # 查询备份记录表数据并进行分页
        records = BackupRecord.query.paginate(page=page, per_page=per_page, error_out=False)
        records_list = [record.to_dict() for record in records.items]

        return jsonify({
            'code': 0,
            'message': 'Backup records retrieved successfully',
            'data': records_list,
            'admin_name': admin_name,
            'total': records.total,  # 总条目数
            'pages': records.pages,  # 总页数
            'current_page': records.page  # 当前页码
        })
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': 'Failed to retrieve backup records',
            'data': None
        })

# 管理员进行数据库备份服务函数
def create_backup():
    """
    进行数据库备份

    返回:
        JSON 响应: 包含备份结果的 JSON 对象
    """
    try:
        # 获取当前管理员身份
        admin_id = get_jwt_identity().get('user_id')

        # 查询管理员的备份设置
        setting = BackupSetting.query.filter_by(admin_id=admin_id).first()

        # 检查是否有备份路径设置
        if not setting or not setting.backup_path:
            return jsonify({
                'code': -2,
                'message': 'Backup path not set',
                'data': None
            })

        # 备份文件的路径和文件名
        backup_dir = setting.backup_path

        # 检查并创建备份目录
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # 构建备份文件路径
        backup_file = os.path.join(backup_dir, f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")
        file_name = os.path.basename(backup_file)

        # MySQL 可执行文件的路径和数据库连接信息
        mysqldump_path = 'mysqldump'  # 假设 mysqldump 已经添加到系统路径
        username = 'root'  # MySQL 用户名
        password = '1234'  # MySQL 密码
        database_name = 'retrievalsystem'  # 数据库名称
        host = 'localhost'  # 数据库主机

        # mysqldump 导出命令
        command = [
            mysqldump_path,
            '-u', username,
            f'-p{password}',  # 密码直接跟在 -p 后面
            '-h', host,
            database_name,
            '--result-file', backup_file  # 指定导出的文件路径
        ]

        # 执行导出命令
        subprocess.run(command, check=True)

        # 保存备份记录到数据库
        backup_record = BackupRecord(
            admin_id=admin_id,
            backup_date=datetime.datetime.now(),
            backup_filename=file_name,
        )
        db.session.add(backup_record)
        db.session.commit()

        return jsonify({
            'code': 0,
            'message': 'Database backup successful',
            'data': backup_record.to_dict()
        })

    except subprocess.CalledProcessError as e:
        db.session.rollback()  # 如果备份失败，回滚事务
        return jsonify({
            'code': -1,
            'message': 'Database backup failed',
            'data': None
        })
    except Exception as e:
        db.session.rollback()  # 如果出现其他异常，回滚事务
        return jsonify({
            'code': -1,
            'message': 'Backup failed',
            'data': None
        })
