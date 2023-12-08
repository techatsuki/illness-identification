from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    diseases = db.Column(db.String(50))
    city    =db.Column(db.String(50))
    address =db.Column(db.String(500))
    phone   =db.Column(db.String(50))
    dob     =db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True    )
    password = db.Column(db.String(150))
    work_type=db.Column(db.String(50))
    phone = db.Column(db.String(12), unique=True)
    city=db.Column(db.String(50))
    first_name = db.Column(db.String(150))
    detail=db.relationship('details')
