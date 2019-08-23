from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from catalog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from catalog.main.routes import main
    from catalog.users.routes import users
    from catalog.books.routes import books

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(books)

    return app
