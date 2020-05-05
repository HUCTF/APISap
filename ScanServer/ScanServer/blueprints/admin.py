from ScanServer.forms import NameForm, ScipyForm, PrintLogForm, LoginForm, RegisterForm
from ScanServer.utils import get_net, get_txt_file, redirect_back
from ScanServer.models import User
from ScanServer.extensions import db

from flask import render_template, request, flash, redirect, url_for , session, jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user, 
from flask_principal import Permission

from threading import Thread
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login')
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        password = form.password.data
        remember = form.remember.data
        user = [User.query.filter(User.username==username_or_email).first(), User.query.filter(User.email==username_or_email).first()]
        print(user)
        if user[0]:
            if user[0].validate_password(password) and user[0].is_super:
                login_user(user[0], remember)
                flash('Welcome back.', 'info')
                return redirect_back()
        elif user[1]:
            if user[1].validate_password(password) and user[0].is_super:
                login_user(user[1], remember)
                flash('Welcome back.', 'info')
                return redirect_back()
        else:
            flash('No account.', 'warning')
    return render_template('login.html', form=form)

@admin_bp.route('/user/list')
@login_required
def user_list():
    if current_user.is_super and current_user.is_authenticated():
        all_user = User.

    return redirect_back()
