import os
basedir = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_DEFAULT_DEST = TOP_LEVEL_DIR + '/app/static/img/'
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/img/'
    UPLOADED_IMAGES_DEST = TOP_LEVEL_DIR + '/app/static/img/'
    UPLOADED_IMAGES_URL = 'http://localhost:5000/static/img/'
