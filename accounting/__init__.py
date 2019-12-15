from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from accounting.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    # Setup Flask and read config from Config Class defined above
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)

    # ReCAPTCHA is always true
    app.testing = True

    # Initialize Flask extensions
    mail.init_app(app)  # Initialize Flask-Mail
    db.init_app(app)  # Initialize Flask-SQLAlchemy
    bcrypt.init_app(app)  # Initialize Flask-Bcrypt
    login_manager.init_app(app)  # Initialize Flask-Login

    # Import application structure
    from accounting.users.routes import users
    from accounting.posts.routes import posts
    from accounting.main.routes import main
    from accounting.errors.handlers import errors

    # Register imported blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # Return application
    return app
