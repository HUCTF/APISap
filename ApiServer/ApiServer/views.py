# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for , session
from threading import Thread
import os

from ApiServer import app
from ApiServer.forms import LoginForm, RegisterForm
from ApiServer.models import User
from ApiServer.utils import redirect_back

@app.route('/')
def index():
    return 'hello, world'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password1 = form.password1.data
        if not all([username, password, password1]):
            flash('请把信息填写完整')
        elif password != password1:
            flash('两次密码不一致，请重新输入！')
        else:
            new_user = User(username=username, password=password, id=None)
            db.session.add(new_user)
            try:
                return redirect(url_for('index'))
                db.session.commit()
            except:
                flash("注册失败，请重试！")
                db.session.rollback()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter(User.username==username, User.validate_password(password)).first()
        print(user.username)
        print(user.password)
        if user:
            login_user(user, remember)
            login_user(user, remember)
            flash('Welcome back.', 'info')
            return redirect_back()
        else:
            flash('No account.', 'warning')
    return render_template('login.html', form=form)

