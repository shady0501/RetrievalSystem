from flask import Flask
from routes.user import user  # Adjusted import for blueprint
from routes.search import search
from config import app
from flask_cors import CORS
from routes.faq import faq
from routes.admin import admin

# 确保在注册蓝图前加载所有模型
with app.app_context():
    app.register_blueprint(user, url_prefix="/user")
    app.register_blueprint(search, url_prefix="/search")
    app.register_blueprint(faq, url_prefix="/faq")
    app.register_blueprint(admin, url_prefix="/admin")
CORS(app)

if __name__ == '__main__':
    app.run()
