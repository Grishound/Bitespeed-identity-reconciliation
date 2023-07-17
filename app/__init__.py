from flask import Flask
from .models import db
from .functions import get_existing_primary_contacts, return_response
from flask_json import FlaskJSON

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
db.init_app(app)
FlaskJSON(app)

from app import routes

# Create the database tables
with app.app_context():
    db.create_all()
