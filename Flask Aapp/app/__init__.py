#import login as login
from flask import Flask
from flask_debug import Debug
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
#from flask.ext.login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# Configure the image uploading via Flask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

Debug(app)
if __name__ == '__main__':
    app.run(debug=True)


from app import routes, models