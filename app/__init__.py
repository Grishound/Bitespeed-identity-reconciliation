import os
from flask import Flask
from .models import db
from .functions import get_existing_primary_contacts, return_response
from flask_json import FlaskJSON

app = Flask(__name__)


#render database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

db.init_app(app)
FlaskJSON(app)

from app import routes
