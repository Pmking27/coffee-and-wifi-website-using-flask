from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from typing import Union

db = SQLAlchemy()


class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), unique=False, nullable=False)
    img_url = db.Column(db.String(250), unique=False, nullable=False)
    location = db.Column(db.String(250), unique=False, nullable=False)
    has_sockets = db.Column(db.Boolean, unique=False, nullable=False)
    has_toilet = db.Column(db.Boolean, unique=False, nullable=False)
    has_wifi = db.Column(db.Boolean, unique=False, nullable=False)
    can_take_calls = db.Column(db.Boolean, unique=False, nullable=False)
    seats = db.Column(db.String(250), unique=False, nullable=True)
    coffee_price = db.Column(db.String(250), unique=False, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)


def read_user(email: str) -> User:
    return User.query.filter_by(email=email).first()


def read_cafe(name: str) -> Cafe:
    return Cafe.query.filter_by(name=name).first()


def create_record(data: Union[User, Cafe]):
    db.session.add(data)
    db.session.commit()