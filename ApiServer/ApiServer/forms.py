# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Required, Email

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
#     password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
#     remember = BooleanField('Remember me')
#     submit = SubmitField('Log in')


# class RegisterForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
#     password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
#     password1 = PasswordField('Re Password', validators=[DataRequired(), Length(1, 128)])
#     submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username_or_email = StringField('Username / Email', validators=[DataRequired('请输入用户名/邮箱')])
    password = PasswordField('Password', validators=[DataRequired('请输入密码'), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired('请输入邮箱'), Email('邮箱格式不正确')])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    password1 = PasswordField('Re Password', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Register')
