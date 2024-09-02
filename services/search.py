from models.image import Image
from models.text import Text
from flask import jsonify
import requests

# 文本检索服务函数
def text_search(keywords):
    # 调用大模型接口，假设接口返回包含图片路径的字典
    try:
        response = requests.post('http://large-model-api-endpoint.com/search', data={'keywords': keywords})
        response_data = response.json()
        image_paths = response_data.get('image_paths', [])
    except Exception as e:
        print(f"调用大模型接口失败: {e}")
        return jsonify({'code': -1,
                        'message': '调用大模型接口失败',
                        'data': None
        })

    # 根据返回的图片路径在数据库中查询对应的图片信息
    image_list = []
    for path in image_paths:
        image = Image.query.filter_by(path=path).first()
        if image:
            image_list.append(image.to_dict())

    return jsonify({'code': 0,
                    'message': '检索成功',
                    'data': image_list
    })

# 图片检索服务函数
def image_search(image_file):
    # 调用大模型接口，假设接口返回包含文本内容的字典
    try:
        files = {'image_file': image_file}
        response = requests.post('http://large-model-api-endpoint.com/image_search', files=files)
        response_data = response.json()
        text_ids = response_data.get('text_ids', [])
    except Exception as e:
        print(f"调用大模型接口失败: {e}")
        return jsonify({
            'code': -1,
            'message': '调用大模型接口失败',
            'data': None
        })

    # 根据返回的文本ID在数据库中查询对应的文本信息
    text_list = []
    for text_id in text_ids:
        text = Text.query.filter_by(id=text_id).first()
        if text:
            text_list.append(text.to_dict())

    return jsonify({
        'code': 0,
        'message': '检索成功',
        'data': text_list
    })