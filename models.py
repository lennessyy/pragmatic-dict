from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
from sqlalchemy_utils import PasswordType

db = SQLAlchemy()

# bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)

    password = db.Column(PasswordType(
            schemes=['pbkdf2_sha512']
        ), nullable=False)

    email = db.Column(db.String(50), nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        '''Create a new user and return the created user'''

        return cls(username=username, password=pwd, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        '''Authenticate a user when they attempt to login'''
        user = User.query.filter(User.username==username).one()

        if user and user.password == pwd:
            # return the user
            return user
        else:
            return False


class Search(db.Model):
    __tablename__ = 'searches'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    word = db.Column(db.String(100), nullable=False)

    note = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref="searches")

