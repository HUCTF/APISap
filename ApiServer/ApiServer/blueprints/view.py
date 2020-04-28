# -*- coding: utf-8 -*-
from flask import render_template,  Blueprint, session
from flask_login import login_required, current_user, login_user, logout_user
from threading import Thread
import os

from ApiServer.utils import redirect_back

view_bp = Blueprint('view', __name__)

@view_bp.route('/init_ip', methods=['GET', 'POST'])
@login_required
def init_ip():
    session['init_ip']='success'
    return render_template('view/init_ip.html')

@view_bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if session['init_ip']:
    
        return render_template('view/index.html')
    else:
        return redirect_back()
