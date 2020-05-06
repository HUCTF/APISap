from ScanServer.forms import NameForm, ScipyForm, PrintLogForm, LoginForm, RegisterForm, InitForm, CookieForm, AimUserForm
from ScanServer.utils import get_net, redirect_back, write_env, initenv_userfile
from ScanServer.models import User
from ScanServer.extensions import db

from flask import render_template, request, flash, redirect, url_for , session, jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

from threading import Thread
import os

import docker


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
        

def build_docker1():
    client = docker.from_env()
    user_container = client.containers.run(
        image="xxxxx",
        command="python /opt/scanSpider.py %s" % current_user.username,
        volumes={'/opt/scanspider/user/%s' % current_user.username:{
                                                                'bind':'/opt/scanspider/%s' % current_user.username,'mode':'rw'
                                                            }},
        name='scanserver-%s' % current_user.username,
        working_dir='/opt/spicer',
#         detach=True,
#         stdout=True,
#         stderr=True,
#         user='root',
#         remove=False
    )
    wait_container(client, user_container)
    print(str(user_container.logs()))
    user_container.remove()




#  -------------------------------------
#  -------------------------------------
#  -------------------------------------
#  -------------------------------------
#  -------------------------------------
#  -------------------------------------

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
    # os.system('kubectl create -f [path/kube.yml]')
    if current_user.is_authenticated:
        os.system('docker run -id --env-file=userfile_center/{0}/{0}_env/.env -v /root/2020-Works-ApiSecurity/ScanServer/userfile_center/{0}/{0}_spider:/opt/scanspider/{0} --name scanserver-{0} python:3.7-alpine tail -f'.format(username))


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
        build_docker(current_user.username)
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
        
        env_head = ['USERNAME={}\n'.format(current_user.username), 'RUNWAY={}\n'.format(runway)]
        write_env(current_user.username, env_list=env_head, flag='w')

        if form.validate_on_submit():
            if form.spider.data:
                print('kaishi')
                flash('开始重发！')
                print('重发')
#                env_list = ['USERNAME={}\n'.format(current_user.username, 'RUNWAY={}\n'.format(runway)]
                env_body = ['USERCOOKIE1={}\n'.format(usercookie1), 'USERCOOKIE2={}\n'.format(usercookie2)]
                write_env(current_user.username, env_list=env_body, flag='a')



        return render_template("user/pcap.html", website=website, form=form)



    elif session.get('runway') == 'userid':

        form = AimUserForm()
        stop = 1



        if form.validate_on_submit():
            if form.spider.data:
                print('kaishi')
                flash('开始重发！')
                print('重发')



        return render_template("user/pcap.html", website=website, form=form)

    return redirect(url_for('user.index'))



# @user_bp.route("/pcap1", methods=['GET', 'POST'])
# @login_required
# def pcap1():
#     # form = NameForm()
#     # form1 = PrintLogForm()
#     stop = 1
#     if session.get('website'):
#         form = WorkForm()
#         website = session.get('website')
#         runway = session.get('runway')
#         if form.validate_on_submit():
#             if form.spider.data:
#                 print('kaishi')
#                 # import time
#                 # from ScanServer.scanapi.v4.NIC_package_get import NICRUN
#                 # stop = 0
#                 # flash('开始抓包！')
#                 # print("=========================",netname, 1000, current_user.username)
#                 # thread = Thread(target=NICRUN, args=[netname, 1000, str(current_user.username)])
#                 # # 使用多线程
#                 # thread.start()
#                 # time.sleep(0.5)
#                 # from ScanServer.scanapi.v4.scanapi import RQRUN
#                 # stop = 0
#                 # flash('开始爬虫！')
#                 # thread = Thread(target=RQRUN)
                
#                 # # 使用多线程
#                 # thread.start()
                
#                 # build_docker1()

                
# # ---------------------------------------------------------------------
# # ---------------------------------------------------------------------
# # ---------------------------------------------------------------------
# # ---------------------------------------------------------------------
# # ---------------------------------------------------------------------
#                 # thread = Thread(target=send_async_email, args=[app, message])
#                 # # 使用多线程
#                 # thread.start()
#                 flash('开始重发！')
#                 print('重发')
#         return render_template("user/pcap.html", website=website, form=form)
#     return redirect(url_for('user.index'))



# @user_bp.route("/net", methods=["GET", "POST"])
# @login_required
# def net():
#     form = NameForm()
#     # netnames = get_net()
#     # net = [(netname[0],netname[0]+' ---- '+netname[1]) for netname in netnames]
#     # form.netname.choices = net
#     if form.validate_on_submit():
#         netname = form.netname.data
#         needpcap = form.needpcap.data
#         session['netname'] = netname
#         session['needpcap'] = needpcap
#         return redirect(url_for('user.pcap', netname=netname, needpcap=needpcap))
#     return render_template('net.html', form=form)

# @user_bp.route("/pcap", methods=['GET', 'POST'])
# @login_required
# def pcap():
#     form = NameForm()
#     form1 = PrintLogForm()
#     netname = request.args.get("netname", None)
#     needpcap = request.args.get("needpcap", None)
#     stop = 1
#     if session.get('netname') and session.get('needpcap'):
#         form = ScipyForm()
#         netname = session.get('netname')
#         needpcap = session.get('needpcap')
#         if form.validate_on_submit():
#             if form.scipy.data:
#                 from ScanServer.scanapi.v4.NIC_package_get import NICRUN
#                 stop = 0
#                 flash('开始抓包！')
#                 print("=========================",netname, needpcap, current_user.username)
#                 thread = Thread(target=NICRUN, args=[netname, needpcap, str(current_user.username)])
#                 # 使用多线程
#                 thread.start()

#             elif form.spider.data:
                
#                 from ScanServer.scanapi.v4.scanapi import RQRUN
#                 stop = 0
#                 flash('开始爬虫！')
#                 thread = Thread(target=RQRUN)
                
#                 # 使用多线程
#                 thread.start()

#             elif form.repeter.data:
#                 thread = Thread(target=send_async_email, args=[app, message])
#                 # 使用多线程
#                 thread.start()
#                 flash('开始重发！')
#         return render_template("pcap.html", netname=netname, needpcap=needpcap, form=form, stop=stop, form1=form1)
#     return redirect(url_for('user.net'))
    

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

