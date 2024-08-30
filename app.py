from flask import Flask
from routes.user import user  # Adjusted import for blueprint
from config import app
from flask_cors import CORS

# 确保在注册蓝图前加载所有模型
with app.app_context():
    app.register_blueprint(user, url_prefix="/user")

CORS(app)

if __name__ == '__main__':
    app.run()
