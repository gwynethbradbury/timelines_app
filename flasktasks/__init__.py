from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dbconfig

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}@{}/timelines'\
    .format(dbconfig.db_user,
            dbconfig.db_hostname)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/timelines'\
#     .format(dbconfig.db_user,
#             dbconfig.db_password,
#             dbconfig.db_hostname)


app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)


import flasktasks.views
import flasktasks.filters
import flasktasks.plugin_filters
import flasktasks.models
import flasktasks.logger


from flasktasks.plugins import load_plugins

load_plugins()
