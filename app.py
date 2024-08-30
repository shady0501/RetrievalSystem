from flask import Flask
from routes.user import user
from config import app
from flask_cors import CORS

app.register_blueprint(user, url_prefix="/user")

CORS(app)

if __name__ == '__main__':
    app.run()
