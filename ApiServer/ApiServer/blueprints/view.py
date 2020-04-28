# -*- coding: utf-8 -*-
from flask import render_template,  Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from threading import Thread
import os


view = Blueprint('view', __name__)

@view.route('/init_ip', methods=['GET', 'POST'])
def init_ip():
    return render_template('init_ip.html')

@view.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
