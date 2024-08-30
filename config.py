from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 连接数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:110119XPY@127.0.0.1:3306/retrievalsystem'

# 数据库连接对象
db_init = SQLAlchemy(app)
