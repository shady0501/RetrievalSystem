import os  # 导入 os 模块用于文件操作
import time  # 导入 time 模块用于时间戳生成
from flask import request, jsonify  # 导入 Flask 模块用于处理请求和生成响应
from PIL import Image  # 导入 PIL 库用于图片处理

# 配置用户上传文件夹和允许的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 允许的图片类型
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB 最大上传文件大小

# 检查文件是否符合允许的扩展名格式
def allowed_file(filename):
    """
    检查文件是否符合允许的扩展名格式

    参数:
        filename (str): 文件名

    返回:
        bool: 如果文件扩展名被允许则返回 True，否则返回 False
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 保存上传的文件并处理图片（如调整大小）
def save_and_process_file(file, upload_folder):
    """
    保存上传的文件并处理图片（如调整大小）

    参数:
        file (FileStorage): 上传的文件对象
        upload_folder (str): 上传文件保存的文件夹路径

    返回:
        str: 保存处理后的图片文件路径，如果文件类型不允许则返回 None
    """
    if file and allowed_file(file.filename):
        # 生成带时间戳的文件名，并保留原始文件扩展名
        extension = file.filename.rsplit('.', 1)[1].lower()
        timestamp = int(time.time())
        filename = f"{timestamp}.{extension}"
        file_path = os.path.join(upload_folder, filename)

        # 保存原始图片
        file.save(file_path)

        # 打开图片进行处理，例如调整大小
        try:
            with Image.open(file_path) as img:
                img = img.resize((200, 200))  # 将图片调整为 200x200 像素
                img.save(file_path)  # 保存处理后的图片
        except Exception as e:
            return None

        return file_path
    return None

# 确保上传文件的目录存在，如果不存在则创建该目录
def ensure_upload_folder_exists(upload_folder):
    """
    确保上传文件的目录存在，如果不存在则创建该目录

    参数:
        upload_folder (str): 上传文件保存的文件夹路径
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

# 处理文件上传的主函数，用于在 Flask 路由中调用
def handle_file_upload(upload_folder, file_field_name):
    """
    处理文件上传的主函数，用于在 Flask 路由中调用

    参数:
        upload_folder (str): 上传文件保存的文件夹路径
        file_field_name (str): 表单中文件字段的名称

    返回:
        JSON 响应: 包含上传结果的 JSON 对象
    """
    # 确保上传文件夹存在
    ensure_upload_folder_exists(upload_folder)

    # 检查请求中是否包含文件部分
    if file_field_name not in request.files:
        return jsonify({
            'code': -1,
            "message": "No file has been uploaded",
            "data": None
        })

    # 获取上传的文件
    file = request.files[file_field_name]

    # 检查文件大小
    if file.content_length > MAX_CONTENT_LENGTH:
        return jsonify({
            'code': -2,
            "message": f"The file is too large. The maximum allowed size is {MAX_CONTENT_LENGTH / (1024 * 1024)} MB.",
            "data": None
        })

    # 保存并处理图片
    file_path = save_and_process_file(file, upload_folder)
    if file_path:
        return jsonify({
            'code': 0,
            "message": "Image upload successful.",
            "data": {"file_path": file_path}
        })
    else:
        return jsonify({
            'code': -3,
            "message": "The file type is not allowed or the image processing failed",
            "data": None
        })
