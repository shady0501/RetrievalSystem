import os
import time
from flask import request, jsonify, current_app
from PIL import Image

# 配置上传文件夹和允许的文件类型

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 允许的图片类型
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB 最大上传文件大小

# 检查文件是否符合允许的扩展名格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 保存上传的文件并处理图片（如调整大小）
def save_and_process_file(file, upload_folder):
    if file and allowed_file(file.filename):
        # 生成带时间戳的文件名，并保留原始文件扩展名
        extension = file.filename.rsplit('.', 1)[1].lower()
        timestamp = int(time.time())
        filename = f"{timestamp}.{extension}"
        file_path = os.path.join(upload_folder, filename)

        # 保存原始图片
        file.save(file_path)

        # 打开图片进行处理，例如调整大小
        with Image.open(file_path) as img:
            img = img.resize((200, 200))  # 将头像图片调整为 200x200 像素
            img.save(file_path)  # 保存处理后的图片

        return file_path
    return None

# 确保上传文件的目录存在，如果不存在则创建该目录
def ensure_upload_folder_exists(upload_folder):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

# 处理文件上传的主函数，用于在 Flask 路由中调用
def handle_file_upload(upload_folder):
    # 确保上传文件夹存在
    ensure_upload_folder_exists(upload_folder)

    # 检查请求中是否包含文件部分
    if 'avatar' not in request.files:
        return jsonify({
            'code': -1,
            "message": "没有文件被上传",
            "data": None
        })

    # 获取上传的文件
    file = request.files['avatar']

    # 检查文件大小
    if file.content_length > MAX_CONTENT_LENGTH:
        return jsonify({
            'code': -2,
            "message": f"文件太大，最大允许 {MAX_CONTENT_LENGTH / (1024 * 1024)}MB",
            "data": None
        })

    # 保存并处理头像图片
    file_path = save_and_process_file(file, upload_folder)
    current_directory = os.getcwd()
    print(f"当前工作目录: {current_directory}")
    if file_path:
        return jsonify({
            'code': 0,
            "message": "头像上传成功",
            "data": {"file_path": file_path}
        })
    else:
        return jsonify({
            'code': -3,
            "message": "不允许的文件类型",
            "data": None
        })