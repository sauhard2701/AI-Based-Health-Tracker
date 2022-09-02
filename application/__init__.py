from flask import Flask
from application.utils import UPLOADS_FOLDER

app = Flask(__name__)
app.config['SECRET_KEY'] = '75f99765ab52e13194e112135e67e46cbac2d56f'
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER

from application import routes
