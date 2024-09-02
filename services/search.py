from models.image import Image
from models.search_history import SearchHistory
from models.text import Text
from config import db_init as db
from flask_login import current_user
from datetime import datetime
from flask import jsonify
import requests



# 文本检索服务函数
def text_search(keywords):
    # # 调用大模型接口，假设接口返回包含图片路径的字典
    # try:
    #     response = requests.post('http://large-model-api-endpoint.com/search', data={'keywords': keywords})
    #     response_data = response.json()
    #     image_paths = response_data.get('image_paths', [])
    # except Exception as e:
    #     print(f"调用大模型接口失败: {e}")
    #     return jsonify({'code': -1,
    #                     'message': '调用大模型接口失败',
    #                     'data': None
    #     })

    # 假装调用大模型接口，返回一个测试结果
    print("模拟调用大模型接口进行文本检索")
    # 模拟的图片路径结果
    image_paths = ['/path/to/image1.jpg', '/path/to/image2.jpg']


    # 根据返回的图片路径在数据库中查询对应的图片信息
    image_list = []
    for path in image_paths:
        # image = Image.query.filter_by(path=path).first()
        # if image:
        #     image_list.append(image.to_dict())

        # 使用模拟的图片路径数据
        image_list = []
        for path in image_paths:
            # 使用模拟数据，不需要真正查询数据库
            image_list.append({
                'id': 1,  # 假设图片ID
                'path': path,
                'description': '模拟图片描述',
                'source': '模拟来源',
                'format': 'jpg',
                'resolution': '1920x1080'
            })

        # 将查询到的图片路径转换为字符串以存储在search_pictur
        search_pictur = ','.join(image_paths)

        # 创建检索历史记录
        new_history = SearchHistory(
            user_id=current_user.id,
            date=datetime.now(),
            search_type=0,  # 文本检索
            search_text=keywords,
            search_pictur=search_pictur
        )
        db.session.add(new_history)
        db.session.commit()

    return jsonify({'code': 0,
                    'message': '检索成功',
                    'data': image_list
    })

# 图片检索服务函数
def image_search(image_file):
    # # 调用大模型接口，假设接口返回包含文本内容的字典
    # try:
    #     files = {'image_file': image_file}
    #     response = requests.post('http://large-model-api-endpoint.com/image_search', files=files)
    #     response_data = response.json()
    #     text_ids = response_data.get('text_ids', [])
    # except Exception as e:
    #     print(f"调用大模型接口失败: {e}")
    #     return jsonify({
    #         'code': -1,
    #         'message': '调用大模型接口失败',
    #         'data': None
    #     })

    # 假装调用大模型接口，返回一个测试结果
    print("模拟调用大模型接口进行图片检索")
    # 模拟的文本ID结果
    text_ids = [1, 2]

    # 使用模拟的文本ID数据
    text_list = []
    for text_id in text_ids:
        # 使用模拟数据，不需要真正查询数据库
        text_list.append({
            'id': text_id,
            'title': '模拟文本标题',
            'content': '这是模拟的文本内容',
            'source': '模拟来源'
        })

    # 将文本ID转换为逗号分隔的字符串以存储在search_text
    search_text = ','.join(map(str, text_ids))

    # # 根据返回的文本ID在数据库中查询对应的文本信息
    # text_list = []
    # for text_id in text_ids:
    #     text = Text.query.filter_by(id=text_id).first()
    #     if text:
    #         text_list.append(text.to_dict())

    # 将上传的文件名作为search_pictur来存储
    search_pictur = image_file.filename

    # 创建检索历史记录
    new_history = SearchHistory(
        user_id=current_user.id,
        date=datetime.now(),
        search_type=1,  # 图片检索
        search_text=search_text,  # 使用模拟的文本ID
        search_pictur=search_pictur  # 使用上传的文件名
    )
    db.session.add(new_history)
    db.session.commit()

    return jsonify({
        'code': 0,
        'message': '检索成功',
        'data': text_list
    })