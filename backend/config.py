from datetime import timedelta
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_PASSWORD = '1'
    JWT_SECRET_KEY = 'anything-you-want'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)