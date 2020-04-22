from ScanServer.util import get_txt_file

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

