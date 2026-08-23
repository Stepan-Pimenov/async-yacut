import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
