from flask import Flask, jsonify  # 导入 Flask 和 jsonify 模块
from flask_sqlalchemy import SQLAlchemy  # 导入 SQLAlchemy 用于数据库操作
from flask_jwt_extended import JWTManager  # 导入 JWTManager 用于 JWT 处理

# 创建 Flask 应用实例
app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/test'  # 设置数据库 URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用修改跟踪以减少开销

# JWT 配置
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 设置 JWT 密钥，建议使用随机生成的安全密钥

# 初始化数据库对象
db_init = SQLAlchemy(app)

# 初始化 JWT
jwt = JWTManager(app)


