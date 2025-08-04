from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User
from .routes import main
from .admin_routes import admin

login_manager = LoginManager()
login_manager.login_view = 'admin.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
    app.config['SECRET_KEY'] = 'secret123'

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    return app
