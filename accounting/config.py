import os


class Config:
    # Flask settings
    SECRET_KEY = 'fc8c5975487d7c08dede678b7bece09a'  # should be in env variables
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # should be in env variables
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # needs to add credentials to SMTP
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # needs to add credentials to SMTP
