from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

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
    from app.users.routes import users
    from app.posts.routes import posts
    from app.companies.routes import companies
    from app.invoices.routes import invoices
    from app.main.routes import main
    from app.errors.handlers import errors

    # Register imported blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(companies)
    app.register_blueprint(invoices)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # Setup jinja2 filter
    from app.filters import payment_converter, type_converter
    app.jinja_env.filters['payment_converter'] = payment_converter
    app.jinja_env.filters['type_converter'] = type_converter

    # Return application
    return app
