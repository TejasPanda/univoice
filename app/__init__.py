import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth  # <--- 1. NEW IMPORT
from config import Config


db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()  # <--- 2. INITIALIZE

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' 

    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

    from app.routes import main
    app.register_blueprint(main)

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ✅ AUTO CREATE TABLES + SEED
    with app.app_context():
        db.create_all()

        from seed import seed_data
        seed_data()

    return app