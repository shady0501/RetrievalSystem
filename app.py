from flask import Flask
from routes.user import user  # User blueprint
from routes.search_history import search_history
from routes.search import search
from routes.faq import faq
from routes.admin import admin
from config import app  # Import the app from config.py
from flask_cors import CORS

# Register blueprints
with app.app_context():
    app.register_blueprint(user, url_prefix="/user")
    app.register_blueprint(search, url_prefix="/search")
    app.register_blueprint(faq, url_prefix="/faq")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(search_history, url_prefix="/search_history")

CORS(app)

if __name__ == '__main__':
    app.run()
