#-*- coding:utf-8 -*-
from flask import Flask
from flask import  jsonify, Blueprint
from flask_login import login_required
# import win_inet_pton

app = Flask(__name__)
# app.config["SERVER_NAME"] = 'tokiesgiao.cc:5000'

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/')
def api_index():
    return jsonify(message='hello, world!, api')

@api_v1.route('/hello')
@login_required
def aa()
    return jsonify(message='hello, vip!') 

# app.register_blueprint(api_v1, url_prefix='/api/v1')
# app.register_blueprint(api_v1, subdomain='api', url_prefix='/v1')
