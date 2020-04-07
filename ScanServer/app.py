#coding:utf-8
from flask import Flask, render_template_string
from flask import render_template, request, flash, redirect, url_for , session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Required
from flask_bootstrap import Bootstrap

from threading import Thread
import psutil

def get_net():
    '''
    获取当前机器所有的网卡名
    return [('网卡名', 'ip'), (), ...]
    '''
    netcard_info=[]
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and not item[1][:3] != '192':
                netcard_info.append((k, item[1]))
    return netcard_info




app = Flask(__name__)
app.config[ "SECRET_KEY"] =  "s_e_c_r_e_t_k_e_y_h_u_c_t_f"
bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    # text = StringField( "网卡名",validators= [DataRequired()])
    netname = SelectField('网卡名', coerce=str)
    needpcap = StringField('抓包个数', validators=[DataRequired(), Length(1, 10)])
    submit = SubmitField( "提交")

class ScipyForm(FlaskForm):
    scipy = SubmitField("开启抓包")
    spider = SubmitField("开启扫描")
    repeter = SubmitField("重发数据包")

class PrintLogForm(FlaskForm):
    scipylog = TextAreaField("数据包抓取记录",validators=[Required()])
    spiderlog = TextAreaField("爬虫记录",validators=[Required()])
    repeterlog = TextAreaField("重发器记录",validators=[Required()])

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    netnames = get_net()
    net = [(netname[0],netname[0]+' ---- '+netname[1]) for netname in netnames]
    form.netname.choices = net
    if form.validate_on_submit():
        netname = form.netname.data
        needpcap = form.needpcap.data
        session['netname'] = netname
        session['needpcap'] = needpcap
        return redirect(url_for('pcap', netname=netname, needpcap=needpcap))
    return render_template('index.html', form=form)

@app.route("/pcap", methods=['GET', 'POST'])
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
                from scanapi.v2.NIC_package_get import NICRUN
                stop = 0
                flash('开始抓包！')
                
                thread = Thread(target=NICRUN, args=[netname, needpcap])
                # 使用多线程
                thread.start()

            elif form.spider.data:
                from scanapi.v2.scanapi import RQRUN
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
    return redirect(url_for('index'))   

@app.errorhandler(400)
def bad_request(e):
    return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ ==  "__main__":
    app.run(host='0.0.0.0', port=5000)
