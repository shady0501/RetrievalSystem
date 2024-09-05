from flask_jwt_extended import get_jwt_identity
from models.backup_record import BackupRecord
from models.backup_settings import BackupSetting
from config import db_init as db
from flask import jsonify
import datetime
import os
import subprocess
import subprocess
import os
import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.backup_record import BackupRecord
import os
import datetime
import subprocess
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import User


# 获取备份记录服务函数
def get_record(page=1, per_page=100):
    try:
        # 获取当前管理员身份
        admin_id = get_jwt_identity().get('user_id')
        admin_name = User.query.get(admin_id).username

        # 查询备份记录表数据并进行分页
        records = BackupRecord.query.paginate(page=page, per_page=per_page, error_out=False)
        records_list = [record.to_dict() for record in records.items]

        return jsonify({
            'code': 0,
            'message': '获取备份记录成功',
            'data': records_list,
            'admin_name': admin_name,
            'total': records.total,  # 总条目数
            'pages': records.pages,  # 总页数
            'current_page': records.page  # 当前页码
        })
    except Exception as e:
        print(f"获取备份记录失败: {e}")
        return jsonify({
            'code': -1,
            'message': '获取备份记录失败',
            'data': None
        })

# 管理员进行数据库备份服务函数
def create_backup():
    try:
        # 获取当前管理员身份
        admin_id = get_jwt_identity().get('user_id')
        # 根据管理员查询备份路径
        setting = BackupSetting.query.filter_by(admin_id=admin_id).first()

        # 备份文件的路径和文件名
        backup_dir = setting.backup_path
        # 检查并创建备份目录
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # 使用 os.path.join 构建路径，避免双斜杠问题
        backup_file = os.path.join(backup_dir, f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")

        # 抽取文件名
        file_name = os.path.basename(backup_file)

        # MySQL 可执行文件的路径
        mysqldump_path = r'mysqldump'  # 假设 mysqldump 已经添加到系统路径
        username = 'root'  # MySQL 用户名
        password = '110119XPY'  # MySQL 密码
        database_name = 'retrievalsystem'  # 数据库名称
        host = 'localhost'  # 数据库主机，通常是 localhost

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
            'message': '数据库备份成功',
            'data': backup_record.to_dict()
        })

    except subprocess.CalledProcessError as e:
        db.session.rollback()  # 如果备份失败，回滚事务
        print(f"数据库备份失败: {e}")
        return jsonify({
            'code': -1,
            'message': '数据库备份失败',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        print(f"备份失败: {e}")
        return jsonify({
            'code': -1,
            'message': '备份失败',
            'data': None
        })
