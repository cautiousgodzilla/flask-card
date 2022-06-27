from enum import unique
from sqlalchemy.engine import create_engine
from flask_sqlalchemy import SQLAlchemy
from database import db
from flask_security import UserMixin, RoleMixin
from datetime import date
from sqlalchemy.sql import func




roles_users = db.Table('roles_users', 
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')), 
        db.Column('role_id',db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer(), autoincrement = True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    

class Role(db.Model, RoleMixin):
    __tablename__ ='role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class cardecks(db.Model):
    __tablename__='cardecks'
    deck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable =False)
    topic = db.Column(db.String(50))
    last_r = db.Column(db.Date, server_default=date.today().strftime('%Y-%m-%d'), onupdate=date.today().strftime('%Y-%m-%d'), nullable=False)
    #child = db.relationship('flashcard', backref='cardecks')

    def __init__(self, user_id, topic):
        self.user_id = user_id
        self.topic = topic


class flashcard(db.Model):
    __tablename__='cards'
    card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    front = db.Column(db.String(255))
    back = db.Column(db.String(255))
    time = db.Column(db.Date, server_default=date.today().strftime('%Y-%m-%d'), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey("cardecks.deck_id"), nullable =False)
    interval = db.Column(db.Integer, default=1)
 
    def __init__(self, front, back, deck_id):
        #self.student_id = student_id 
        self.front = front
        self.back = back 
        self.time = date.today()
        self.deck_id = deck_id

        


#db.create_all()
