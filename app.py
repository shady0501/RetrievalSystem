from flask import Flask  # 导入 Flask 模块用于创建应用
from flask_cors import CORS  # 导入 CORS 模块用于处理跨域请求
from routes.user import user  # 导入用户蓝图
from routes.search_history import search_history  # 导入检索历史蓝图
from routes.search import search  # 导入搜索蓝图
from routes.faq import faq  # 导入 FAQ 蓝图
from routes.admin import admin  # 导入管理员蓝图
from config import app  # 从 config.py 导入应用实例

# 注册蓝图
with app.app_context():
    app.register_blueprint(user, url_prefix="/user")  # 注册用户蓝图，设置 URL 前缀为 /user
    app.register_blueprint(search, url_prefix="/search")  # 注册搜索蓝图，设置 URL 前缀为 /search
    app.register_blueprint(faq, url_prefix="/faq")  # 注册 FAQ 蓝图，设置 URL 前缀为 /faq
    app.register_blueprint(admin, url_prefix="/admin")  # 注册管理员蓝图，设置 URL 前缀为 /admin
    app.register_blueprint(search_history, url_prefix="/search_history")  # 注册检索历史蓝图，设置 URL 前缀为 /search_history

# 启用跨域资源共享（CORS），允许来自不同域的请求访问此应用
CORS(app)

if __name__ == '__main__':
    # 启动 Flask 应用
    app.run(host="0.0.0.0", debug=True)
