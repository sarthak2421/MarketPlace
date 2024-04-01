from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
# Adding configuration to app of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketdb.db'
app.config['SECRET_KEY'] = '99555c36039b303079813b00'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # To route unsigned user to login page.
login_manager.login_message_category = 'info'
from Market import models
from Market import routes
