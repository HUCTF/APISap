from ScanServer.utils import get_txt_file, api_abort

from flask import render_template, request, flash, redirect, url_for,  jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route('/package', methods=["GET"])
@login_required
def package_msg():
    filename = request.args.get('filename')
    # filename为数据包txt文件名
    # 例如http://127.0.0.1:5000/api/package?filename=文件夹名\文件名
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

@api_v1.route('/deployment/delete', methods=["GET"])
@login_required
def delete_container():
    delete_deployment(current_user.username)
    return jsonify({"result": "delete success", "code":"200"})

@api_v1.route('deployment/pod/status', methods=["GET"])
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

@api_v1.route('deployment/list', methods=['GET', 'POST'])
@login_required
def pod_list():
    if current_user.username == 'admin':
        return "hello"


