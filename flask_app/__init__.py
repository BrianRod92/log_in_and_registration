from flask import Flask
import re
from flask_bcrypt import Bcrypt

# All of your Global variables (meaning any variables that are useful throughout the entire app) are placed in this file. ex. app.secret_key = "pass" <-- this is important any time we import session into one of our controller files.

app = Flask(__name__)
BCRYPT = Bcrypt(app)

DATABASE = "log_in_and_reg_db"

app.secret_key = "watagatapitusberry"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')