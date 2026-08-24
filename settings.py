import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///yacut.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
    DISK_API_HOST = os.getenv(
        'DISK_API_HOST', 'https://cloud-api.yandex.net/'
    )
    DISK_API_VERSION = os.getenv('DISK_API_VERSION', 'v1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
