# Example: using SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    count = db.Column(db.Integer, default=0)
