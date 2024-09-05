from flask_jwt_extended import get_jwt_identity
from models.user import User
from models.personal_interface_setting import PersonalizedInterfaceSetting
from flask import jsonify
from config import db_init as db

# 用户个性化设置功能
def personal_setting(theme,font_style,background_image):
    current_user_id = get_jwt_identity().get('user_id')  # 获取当前用户ID
    u = User.query.filter_by(id=current_user_id, delete_flag=0).first()

    if theme is None and font_style is None and background_image is None:
        return jsonify({
            'code': -10,
            "message": "数据缺失，请重试",
            "data": ""
        })

    user_id = u.id

    s = PersonalizedInterfaceSetting.query.filter_by(user_id=user_id).first()

    # 如果不是第一次存储此用户个性化设置，仅更新
    if s is not None:
        updated = False  # 标记是否有字段更新

        # 更新用户信息字段
        if theme and s.theme != theme:
            s.theme = theme
            updated = True
        if font_style and s.font_style != font_style:
            s.font_style = font_style
            updated = True
        if background_image and s.background_image != background_image:
            s.background_image = background_image
            updated = True

        # 如果没有更新任何字段，返回未修改信息提示
        if not updated:
            return jsonify({
                'code': -100,
                'message': '未修改用户个性化设置信息',
                'data': None
            })

        try:
            db.session.commit()  # 提交数据库会话
            return jsonify({
                'code': 0,
                'message': '用户个性化设置更新成功',
                'data': s.to_dict()
            })
        except Exception as e:
            db.session.rollback()  # 回滚数据库会话
            print(f"更新用户个性化设置失败，数据库操作错误：{e}")
            return jsonify({
                'code': -3,
                'message': '个性化设置更新失败',
                'data': None
            })
    else:
        # 如果是第一次存储
        settings = (PersonalizedInterfaceSetting
                    (user_id=user_id,theme=theme,font_style=font_style,
                     background_image=background_image))

        try:
            db.session.add(settings)
            db.session.commit()  # 提交事务，将数据写入数据库
            return jsonify({
                'code': 0,
                "message": "用户个性化设置成功",
                "data": settings.to_dict()
            })
        except Exception as e:
            db.session.rollback()  # 出现异常时回滚事务
            print("用户个性化设置数据库插入失败：" + str(e))
            return jsonify({
                'code': -3,
                "message": "用户个性化设置失败，请重试",
                "data": ""
            })

