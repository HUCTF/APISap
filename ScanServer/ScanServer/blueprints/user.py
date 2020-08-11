from ScanServer.forms import NameForm, ScipyForm, PrintLogForm, LoginForm, RegisterForm, InitForm, CookieForm, AimUserForm
from ScanServer.utils import get_net, redirect_back, initenv_userfile, get_txt_file
from ScanServer.models import User
from ScanServer.extensions import db
from ScanServer.kube_scanserver import create_deployment, delete_deployment

from flask import render_template, request, flash, redirect, url_for , session, jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

from threading import Thread
import os

import docker
import time

cookie_env = '''
    COOKIE_1=%s
    COOKIE_2=%s
'''
userpswd_env = '''
    USERID=%s
    PASSWD=%s
'''
def wait_container(client, user_container):
    if user_container in client.containers.list(filters={'status':'exited'}):
        with open('/tmp/py_log.txt', 'a') as f:
            f.write(str(user_container.logs()))
    else:
        wait_container()
        


def build_docker(current_user):
    ###############
    ## 新建文件夹 ##
    ###############

    ####################
    ## 具体化template ##
    ####################

    ##################
    ## 保存template ##
    ##################
    # os.system('kubectl create -f [path/kube.yml]')
    if current_user.is_authenticated:
        try:
            try:
                os.system('docker stop scanserver-{0}'.format(current_user.username))
            except:
                pass
            os.system('docker rm scanserver-{0}'.format(current_user.username))
        except:
            pass
        os.system("docker run -id --env-file=userfile_center/{0}/{0}_env/.env -v /opt/2020-Works-ApiSecurity/ScanServer/userfile_center/{0}/{0}_spider:/opt/spider/{0} --name scanserver-{0} scanserver".format(current_user.username))

user_bp = Blueprint('user', __name__)

@user_bp.route("/", methods=["GET", "POST"])
@user_bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    form = InitForm()
    # netnames = get_net()
    # net = [(netname[0],netname[0]+' ---- '+netname[1]) for netname in netnames]
    # form.netname.choices = net
    form.runway.choices = [('cookie', 'by cookie'), ('userid', 'by userid')]
    if form.validate_on_submit():
        website = form.website.data
        runway = form.runway.data
        session['website'] = str(website)
        session['runway'] = runway
        initenv_userfile(current_user, str(website), runway)
#        build_docker(current_user.username)
        return redirect(url_for('user.pcap1'))
    return render_template('user/index.html', form=form)


@user_bp.route("/pcap1", methods=['GET', 'POST'])
@login_required
def pcap1():
    website = session.get('website')
    runway = session.get('runway')


    if session.get('runway') == 'cookie':

        form = CookieForm()
        stop = 1
        usercookie1 = form.usercookie1.data
        usercookie2 = form.usercookie2.data
        if form.validate_on_submit():
            if form.spider.data:
                create_deployment(current_user.username, website, runway, usercookie1, usercookie2)
#                return redirect(url_for("user.result", filename="userfile_center/{0}/{0}_spider/{0}.txt".format(current_user.username)))
                return jsonify({"result": "create success", "code": "200"}) 

        return render_template("user/pcap.html", website=website, form=form)



@user_bp.route('/deployment/delete', methods=["GET"])
@login_required
def delete_container():
    delete_deployment(current_user.username)
    return jsonify({"result": "delete success", "code":"200"})

@user_bp.route('deployment/pod/status', methods=["GET"])
@login_required
def pod_status():
    status = os.system('kubectl -n scanserver get po | grep kies')
    if status == 0:
        return jsonify({
            "result": "RUNNING",
            "code": "200"
        })
    else:
        return jsonify({
            "result": "None",
            "code": "404"
        })

@user_bp.route('deployment/list', methods=['GET', 'POST'])
@login_required
def pod_list():
    if current_user.username == 'admin':
        return 


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

@user_bp.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    filename = request.args.get('filename')
    print("=====result=====")
    print(filename)
    if filename:
        s = get_txt_file(filename)
        return jsonify({
                    'code':'200',
                    'result':str(s),
                    'done':'done',
               })
    else:
        return jsonify({
                    'code':'400',
                    'result':'please input filename!',
               })




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
        elif user[1]:
            if user[1].validate_password(password):
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

