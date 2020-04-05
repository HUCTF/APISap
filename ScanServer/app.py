#coding:utf-8
from flask import Flask, render_template_string
from flask import render_template, request, flash, redirect, url_for , session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap
import base64
import psutil

from scanapi.v1.NIC_package_get import package_print

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

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    netnames = get_net()
    net = [(netname[0],netname[0]+' ---- '+netname[1]) for netname in netnames]
    form.netname.choices = net
    if form.validate_on_submit():
        netname = form.netname.data
        needpacp = form.needpcap.data
        session['you_can_take_it_']=netname
        return redirect(url_for('pacp', netname=netname, needpacp=needpacp))
    return render_template('index.html', form=form)

@app.route("/pacp", methods=['GET', 'POST'])
def pacp():
    form = NameForm()
    netname = request.args.get("netname", None)
    needpacp = request.args.get("needpacp", None)
    if session.get('you_can_take_it_'):
        form = ScipyForm()
        if form.validate_on_submit():
            if form.scipy.data:
                sniff(
                    iface=netname,
                    prn=package_print,
                    lfilter=lambda p: ("GET" in str(p)) or ("POST" in str(p)),
                    filter="tcp")
                    #iface='XXX'  监听本地名为XXX的网卡
                flash('开始抓包！')
                
            elif form.spider.data:
                flash('开始爬虫！')
            elif form.repeter.data:
                flash('开始重发！')
        return render_template("pacp.html", netname=netname, needpacp=needpacp, form=form)
    return redirect(url_for('index'))

@app.errorhandler(400)
def bad_request(e):
    return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ ==  "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
