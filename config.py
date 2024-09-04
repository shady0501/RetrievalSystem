from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:110119XPY@127.0.0.1:3306/retrievalsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Add this line to suppress warnings

# 生成一个安全的随机密钥
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 更改为一个安全的随机密钥

# Initialize the database object
db_init = SQLAlchemy(app)

# Initialize JWT
jwt = JWTManager(app)