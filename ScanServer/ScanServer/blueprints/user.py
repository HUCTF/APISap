from ScanServer.forms import NameForm, ScipyForm, PrintLogForm, LoginForm, RegisterForm
from ScanServer.util import get_net, get_txt_file, redirect_back
from ScanServer.models import User
from ScanServer.extensions import db

from flask import render_template, request, flash, redirect, url_for , session, jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

from threading import Thread
import os


kubenetes_template = '''
    apiVersion: v1
    kind: ReplicaSet
    metadata:
      name: [username]
    spec:
      replicas: 3
      selector:
      matchLabels:
        name:[username]
      template:
        metadata:
          labels:
            name:[username]
        spec:
          containers:
          - name: [username]
            image: [images]
'''

def build_docker(username):
    ###############
    ## 新建文件夹 ##
    ###############

    ####################
    ## 具体化template ##
    ####################

    ##################
    ## 保存template ##
    ##################
    os.system('kubectl create -f [path/kube.yml]')
    

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    return 'hello world'

@user_bp.route("/net", methods=["GET", "POST"])
@login_required
def net():
    form = NameForm()
    # netnames = get_net()
    # net = [(netname[0],netname[0]+' ---- '+netname[1]) for netname in netnames]
    # form.netname.choices = net
    if form.validate_on_submit():
        netname = form.netname.data
        needpcap = form.needpcap.data
        session['netname'] = netname
        session['needpcap'] = needpcap
        return redirect(url_for('user.pcap', netname=netname, needpcap=needpcap))
    return render_template('net.html', form=form)

@user_bp.route("/pcap", methods=['GET', 'POST'])
@login_required
def pcap():
    form = NameForm()
    form1 = PrintLogForm()
    netname = request.args.get("netname", None)
    needpcap = request.args.get("needpcap", None)
    stop = 1
    if session.get('netname') and session.get('needpcap'):
        form = ScipyForm()
        netname = session.get('netname')
        needpcap = session.get('needpcap')
        if form.validate_on_submit():
            if form.scipy.data:
                from ScanServer.scanapi.v3.NIC_package_get import NICRUN
                stop = 0
                flash('开始抓包！')
                print("=========================",netname, needpcap)
                thread = Thread(target=NICRUN, args=[netname, needpcap])
                # 使用多线程
                thread.start()

            elif form.spider.data:
                
                from ScanServer.scanapi.v3.scanapi import RQRUN
                stop = 0
                flash('开始爬虫！')
                thread = Thread(target=RQRUN)
                
                # 使用多线程
                thread.start()

            elif form.repeter.data:
                thread = Thread(target=send_async_email, args=[app, message])
                # 使用多线程
                thread.start()
                flash('开始重发！')
        return render_template("pcap.html", netname=netname, needpcap=needpcap, form=form, stop=stop, form1=form1)
    return redirect(url_for('user.net'))
    

@user_bp.route('/api/package', methods=["GET"])
def package_msg(): 
    filename = request.args.get('filename')
    # filename为数据包txt文件名
    # 例如http://127.0.0.1:5000/api/package?filename=文件夹名\文件名
    s = get_txt_file(filename)
    return jsonify({'code':'200', 'result':str(s)})


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    # register func
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
        username_or_email = form.username_or_email.data
        password = form.password.data
        remember = form.remember.data
        user = [User.query.filter(User.username==username_or_email).first(), User.query.filter(User.email==username_or_email).first()]
        if user[0]:
            if user[0].validate_password(password):
                login_user(user[0], remember)
                login_user(user[0], remember)
                flash('Welcome back.', 'info')
                return redirect_back()
        elif user[1]:
            if user[1].validate_password(password):
                login_user(user[1], remember)
                login_user(user[1], remember)
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
