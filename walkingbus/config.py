import os


class FlaskConfig(object):
    
    # Using environment variable 'SECRET_KEY' if available, else using the key 'development'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'development')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///walkingbus.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
