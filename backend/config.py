from datetime import timedelta
import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_PASSWORD = '1'
    JWT_SECRET_KEY = 'anything-you-want'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(CURRENT_DIR, 'uploads')