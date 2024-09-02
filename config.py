from flask import Flask, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import secrets
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:110119XPY@127.0.0.1:3306/retrievalsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Add this line to suppress warnings

# 设置 secret_key，用于安全性和会话管理
# 生成一个安全的随机密钥
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Initialize the database object
db_init = SQLAlchemy(app)

# 初始化Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 指定登录视图的名称，调整为实际的登录路由
login_manager.login_message = None
login_manager.needs_refresh_message = None

@login_manager.user_loader
def load_user(user_id):
    from models.user import User  # 延迟导入User模型
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        'code': -1,
        'message': '用户未登录',
        'data': None
    }), 401