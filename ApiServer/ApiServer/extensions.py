# -*- coding: utf-8 -*-
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):    
    from ApiServer.models import User
    if User.query.get(int(user_id)) is not None:
        user = User.query.get(int(user_id))
        return user

login_manager.login_view = 'user.login'
# login_manager.login_message = 'Your custom message'
# login_manager.login_message_category = 'warning'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'