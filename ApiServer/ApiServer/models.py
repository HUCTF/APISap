# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

from ApiServer.extensions import db

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    id_md5 = db.Column(db.String(32), unique=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    is_super = db.Column(db.Boolean)

    @staticmethod
    def get_encode_password(userid):
        m = hashlib.md5()
        userid = userid + 'SECRET_KEY'
        m.update(userid.encode())
        return m.hexdigest()
    

    def set_id(self, userid):
        print(self.get_encode_password(userid))
        self.id_md5 = self.get_encode_password(userid)
    
    def check_id(self, userid):
        return self.get_encode_password(userid) == self.id_md5

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


