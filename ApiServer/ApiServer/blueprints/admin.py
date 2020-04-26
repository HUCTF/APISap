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
        return jsonify({
        'code':'200', 
        'username':current_user.username, 
        'is_super': 'True'
        })
    else:
        return jsonify({
            'code':'400', 
            'error':'not admin, not super', 
            'is_super':'False'
            })


# '''
# GET username
# /list/user?username=<name>

# return {
#     "code":"200",
#     "id":"1",
#     "id_md5":"d74f3434668c0d2b45a47e4d78867110",
#     "is_super":"True",
#     "username":"admin"
#     }
# '''
@admin_bp.route('/list/user', methods=['GET'])
@login_required
def list_user():

    if current_user.is_super:
        name = request.args.get('username')
        if not name:
            all_user = User.query.all()
            dict_user = {}
            username = []
            for user in all_user:
                dict_user.setdefault('username', []).append(user.username)

            
            return jsonify({
                'code':'200',
                'all_username': dict_user,
                })
        else:
            user = User.query.filter(User.username==name).one_or_none()
            if user:
                return jsonify({
                    'code': '200',
                    'id': str(user.id),
                    'username': user.username,
                    'id_md5': user.id_md5,
                    'is_super': str(user.is_super)
                })
            else:
                return jsonify({
                    'code':'400',
                    'result':'not found %s.' % name,
                })
    else:
        return jsonify({
            'code':'400', 
            'error':'not admin, not super', 
            'is_super':'False'
        })
