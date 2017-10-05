from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import dbconfig

app = Flask(__name__)

if dbconfig.debug:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}@{}/timelines'\
        .format(dbconfig.db_user,
                dbconfig.db_hostname)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'\
        .format(dbconfig.db_user,
                dbconfig.db_password,
                dbconfig.db_hostname,
                dbconfig.db_port,
                dbconfig.db_name)



app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

import flasktasks.views
import flasktasks.filters
import flasktasks.plugin_filters
import flasktasks.models
import flasktasks.logger
from flasktasks.plugins import load_plugins

load_plugins()



BCRYPT_LOG_ROUNDS = 12

from flask_login import LoginManager
from models import User


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "signin"

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()
