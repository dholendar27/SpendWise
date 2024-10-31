import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Config

load_dotenv()


class DevelopmentConfig(Config):
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS= os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)