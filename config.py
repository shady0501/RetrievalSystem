from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/retrievalsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Add this line to suppress warnings

# Initialize the database object
db_init = SQLAlchemy(app)
