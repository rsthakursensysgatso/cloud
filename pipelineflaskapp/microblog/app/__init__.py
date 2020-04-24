#import login as login
from flask import Flask
from flask_debug import Debug
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
#from flask.ext.login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads
#from flask_session import Session
from flask_kvsession import KVSessionExtension
from flask_mail import Mail, Message



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
mail= Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rsthakur83@gmail.com'
app.config['MAIL_PASSWORD'] = 'Linux@3367'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

login.login_view = 'login'
#sess = Session()
#sess.init_app(app)

# Configure the image uploading via Flask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

Debug(app)
if __name__ == '__main__':
    app.run(debug=True)


from app import routes, models
