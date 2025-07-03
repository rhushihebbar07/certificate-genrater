import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'donotreplay93@gmail.com'
    MAIL_PASSWORD = 'pnai waam mzpp stjd'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
