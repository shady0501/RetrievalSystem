from flask import send_file  # 导入 send_file 用于文件发送
from PIL import Image  # 导入 PIL 库用于图片处理
import os  # 导入 os 模块用于文件操作

# 生成指定格式和分辨率的图片文件
def generate_image(filename, img_format, resolution, base_image_path, temp_image_path):
    """
    根据指定格式和分辨率生成图片文件

    参数:
        filename (str): 原始图片文件名
        img_format (str): 图片格式（如 'JPEG', 'PNG' 等）
        resolution (str): 图片分辨率 ('low', 'medium', 'high')
        base_image_path (str): 原始图片文件的基础路径
        temp_image_path (str): 临时存储生成图片的路径

    返回:
        tuple: 包含新文件名和新文件路径的元组
    """
    # 构建原始文件路径
    original_filepath = os.path.join(base_image_path, filename)

    # 使用 PIL 打开并处理图片
    try:
        img = Image.open(original_filepath)
    except IOError:
        raise FileNotFoundError(f"Cannot find or open the image file: {original_filepath}")

    # 根据选择的分辨率调整图片大小
    resolution_mapping = {
        'low': (640, 480),
        'medium': (1280, 720),
        'high': (1920, 1080)
    }
    if resolution in resolution_mapping:
        img = img.resize(resolution_mapping[resolution])
    else:
        raise ValueError(f"Unsupported resolution: {resolution}")

    # 动态生成新的文件名
    new_filename = f'{os.path.splitext(filename)[0]}_{resolution}.{img_format.lower()}'
    new_filepath = os.path.join(temp_image_path, new_filename)

    # 保存生成的图片
    try:
        img.save(new_filepath, format=img_format.upper())
    except IOError:
        raise IOError(f"Unable to save image file: {new_filepath}")

    return new_filename, new_filepath

# 提供图片文件的下载功能
def send_image(filepath, filename):
    """
    提供图片文件的下载功能

    参数:
        filepath (str): 要发送的文件的路径
        filename (str): 下载时的文件名

    返回:
        文件响应: 使用 send_file 发送文件
    """
    return send_file(filepath, as_attachment=True, download_name=filename)
