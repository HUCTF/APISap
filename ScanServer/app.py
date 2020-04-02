#coding:utf-8
from flask import Flask, render_template_string
from flask import render_template, request, flash, redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import base64
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
    submit = SubmitField( "提交")

class ScipyForm(FlaskForm):
    scipy = SubmitField("开启抓包")
    spider = SubmitField("开启扫描")
    repeter = SubmitField("重发数据包")

@app.route("/")
def index():
    form = NameForm()
    netnames = get_net()
    print(netnames)
    net = [("",netname[0]+' ---- '+netname[1]) for netname in netnames]
    print(net)
    form.netname.choices = net

    return render_template('index.html', form=form)


@app.errorhandler(400)
def bad_request(e):
    return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ ==  "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
