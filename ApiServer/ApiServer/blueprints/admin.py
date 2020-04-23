#-*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for , session, Blueprint, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from threading import Thread
import os

from ApiServer.forms import LoginForm, RegisterForm
from ApiServer.models import User
from ApiServer.utils import redirect_back
from ApiServer.extensions import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def index():
    if current_user.is_super:
        return jsonify({'code':'200', 'username':current_user.username, 'is_super': 'True'})
    else:
        return jsonify({'code':'400', 'error':'not admin, not super', 'is_super':'False'})
