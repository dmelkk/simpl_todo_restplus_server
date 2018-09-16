from .. import db, flask_bcrypt

import datetime
import jwt

from app.auth.model.blacklist import BlacklistToken
from config import key


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    pasword_hash = db.Column(db.String(100))

    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    registered_on = db.Column(db.DateTime, nullable=False)

    @property
    def password(self):
        return AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                    'iat': datetime.datetime.utcnow(),
                    'sub': user_id
                }
            return jwt.encode(
                    payload,
                    key,
                    algorithm='HS256'
                )
        except Exception as e:
            return e

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decode Auth Token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
