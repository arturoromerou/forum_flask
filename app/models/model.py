from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData
import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(40))
    password = db.Column(db.String(66))
    comments = db.relationship('Comment')
    posts = db.relationship('Post')
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.__create_pasword(password)

    def __create_pasword(self, password):
        return bcrypt.generate_password_hash(password).decode ('utf-8')

    '''esta funcion recibe el password en plano y lo compara con el password encriptado en la bd'''
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50))
    text = db.Column(db.Text())
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text())
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

