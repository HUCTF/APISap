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
    return 'hello, world'

@user_bp.route('/vip')
@login_required
def vip():
    return "你好鸭，VIP用户！"

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    # register func
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password1 = form.password1.data
        if not all([username, password, password1]):
            flash('请把信息填写完整')
        elif password != password1:
            flash('两次密码不一致，请重新输入！')
        elif User.query.filter(User.username==username).first():
            flash('这个用户名已经被注册过了！')
        else:
            new_user = User(username=username, id=None)
            new_user.set_password(password)
            db.session.add(new_user)
            # try:
            #     db.session.commit()
                
            #     return redirect(url_for('user.index'))
            # except:
            #     flash("注册失败，请重试！")
            #     db.session.rollback()
            db.session.commit()
            return redirect(url_for('user.index'))
    return render_template('register.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    # login in func
    # if current_user.is_authenticated:
        # return redirect(url_for('user.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter(User.username==username).first()
        if user and user.validate_password(password):
            login_user(user, remember)
            login_user(user, remember)
            flash('Welcome back.', 'info')
            return redirect_back()
        else:
            flash('No account.', 'warning')
    return render_template('login.html', form=form)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()


