from flask import send_file, jsonify
from PIL import Image
import os

# 生成指定格式和分辨率的图片文件
def generate_image(filename, img_format, resolution, base_image_path,temp_image_path):
    # 构建文件路径
    original_filepath = os.path.join(base_image_path, filename)

    # 使用PIL处理图片
    img = Image.open(original_filepath)

    # 根据选择的分辨率调整图片大小
    if resolution == 'low':
        img = img.resize((640, 480))
    elif resolution == 'medium':
        img = img.resize((1280, 720))
    elif resolution == 'high':
        img = img.resize((1920, 1080))

    # 动态生成文件名
    new_filename = f'{os.path.splitext(filename)[0]}_{resolution}.{img_format.lower()}'
    new_filepath = os.path.join(temp_image_path, new_filename)

    # 保存生成的图片
    img.save(new_filepath, format=img_format.upper())

    return new_filename, new_filepath

# 提供图片文件的下载功能
def send_image(filepath, filename):
    return send_file(filepath, as_attachment=True, download_name=filename)
