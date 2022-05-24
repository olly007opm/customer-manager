from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    admin = db.Column(db.Boolean)
    hash = db.Column(db.String(256), nullable=False)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    memberId = db.Column(db.String(256), nullable=False)
    surname = db.Column(db.String(256), nullable=False)
    joined = db.Column(db.Integer, nullable=False)
    membership = db.Column(db.String(256), nullable=False)
    nights = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    bookings = db.relationship('Booking')


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    nights = db.Column(db.Integer, nullable=False)
