from flask_jwt_extended import get_jwt_identity  # 导入 JWT 身份获取方法
from models.user import User  # 导入 User 模型
from models.personal_interface_setting import PersonalizedInterfaceSetting  # 导入个性化设置模型
from flask import jsonify  # 导入 jsonify 用于返回 JSON 响应
from config import db_init as db  # 导入数据库初始化配置

# 用户个性化设置功能
def personal_setting(theme, font_style, background_image):
    """
    用户个性化设置功能

    参数:
        theme (str): 主题
        font_style (str): 字体样式
        background_image (str): 背景图片路径

    返回:
        JSON 响应: 包含操作结果的 JSON 对象
    """
    # 获取当前用户ID
    current_user_id = get_jwt_identity().get('user_id')
    u = User.query.filter_by(id=current_user_id, delete_flag=0).first()

    if not u:
        return jsonify({
            'code': -5,
            "message": "This user does not exist",
            "data": None
        })

    # 检查数据完整性
    if theme is None and font_style is None and background_image is None:
        return jsonify({
            'code': -10,
            "message": "Data missing, please try again",
            "data": None
        })

    user_id = u.id

    # 查询用户的个性化设置
    s = PersonalizedInterfaceSetting.query.filter_by(user_id=user_id).first()

    if s is not None:
        # 更新现有个性化设置
        updated = False  # 标记是否有字段更新

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
                'message': 'User personalization settings not updated',
                'data': None
            })

        try:
            db.session.commit()  # 提交数据库会话
            return jsonify({
                'code': 0,
                'message': 'User personalization settings updated successfully',
                'data': s.to_dict()
            })
        except Exception as e:
            db.session.rollback()  # 回滚数据库会话
            return jsonify({
                'code': -3,
                'message': 'Personalization settings update failed',
                'data': None
            })
    else:
        # 创建新的个性化设置
        settings = PersonalizedInterfaceSetting(
            user_id=user_id,
            theme=theme,
            font_style=font_style,
            background_image=background_image
        )

        try:
            db.session.add(settings)
            db.session.commit()  # 提交事务，将数据写入数据库
            return jsonify({
                'code': 0,
                "message": "User personalization settings successful",
                "data": settings.to_dict()
            })
        except Exception as e:
            db.session.rollback()  # 出现异常时回滚事务
            return jsonify({
                'code': -3,
                "message": "User personalization settings failed, please try again",
                "data": None
            })
