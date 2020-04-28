# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for , session, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from threading import Thread
import os

from ApiServer.forms import LoginForm, RegisterForm
from ApiServer.models import User
from ApiServer.utils import redirect_back
from ApiServer.extensions import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    return render_template('user/hello.html')

@user_bp.route('/vip')
@login_required
def vip():
    return "你好鸭，VIP用户 %s！欢迎回家" % current_user.username

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    # register func
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password1 = form.password1.data
        if not all([username, email, password, password1]):
            flash('请把信息填写完整')
        elif password != password1:
            flash('两次密码不一致，请重新输入！')
        elif User.query.filter(User.username==username).first():
            flash('这个用户名已经被注册过了！')
        elif User.query.filter(User.email==email).first():
            flash('这个邮箱已经被注册过了！')
        else:
            new_user = User(username=username, email=email, id=None)
            new_user.set_id(str(new_user.id))
            new_user.set_password(password)
            db.session.add(new_user)
            # try:
            #     db.session.commit()
                
            #     return redirect(url_for('user.index'))
            # except:
            #     flash("注册失败，请重试！")
            #     db.session.rollback()
            db.session.commit()
            return redirect(url_for('user.login'))
    return render_template('register.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    # login in func
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        password = form.password.data
        remember = form.remember.data
        user = [User.query.filter(User.username==username_or_email).first(), User.query.filter(User.email==username_or_email).first()]
        if user[0]:
            if user[0].validate_password(password):
                login_user(user[0], remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            else:
                flash('账号或者密码错误，请重新输入！', 'warning')
        elif user[1]:
            if user[1].validate_password(password):
                login_user(user[1], remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            else:
                flash('账号或者密码错误，请重新输入！', 'warning')    
        else:
            flash('No account.', 'warning')
    return render_template('login.html', form=form)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()
