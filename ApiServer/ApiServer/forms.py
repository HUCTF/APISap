# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Required

class LoginForm(FlaskForm):
    username = StringField('用户名', coerce=str)
    passwd = 

