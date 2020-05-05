from ScanServer import app
from ScanServer.forms import NameForm, ScipyForm, PrintLogForm
from ScanServer.utils import get_net, get_txt_file

from flask import render_template, request, flash, redirect, url_for , session, jsonify
from threading import Thread
import os

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
    return redirect(url_for('index'))
    

@app.route('/api/package', methods=["GET"])
def package_msg(): 
    filename = request.args.get('filename')
    # filename为数据包txt文件名
    # 例如http://127.0.0.1:5000/api/package?filename=文件夹名\文件名
    s = get_txt_file(filename)
    return jsonify({'code':'200', 'result':str(s)})
