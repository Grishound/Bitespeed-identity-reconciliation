from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    linkedId = db.Column(db.Integer, nullable=True)
    linkPrecedence = db.Column(db.String)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    deletedAt = db.Column(db.DateTime, nullable=True)
