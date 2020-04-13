from flask import Flask
from flask import  jsonify, Blueprint
import win_inet_pton

app = Flask(__name__)
app.config["SERVER_NAME"] = 'tokiesgiao.cc:5000'

api_v1 = Blueprint('api_v1', __name__)
api_v2 = Blueprint('api_v2', __name__)

@api_v1.route('/')
def api_index():
    print("===============hello api==============")
    return jsonify(message='hello, world!, api')



@api_v2.route('/<>')

@api_v2.route('/')
def api2_index():
    





app.register_blueprint(api_v1, url_prefix='/api/v1')
app.register_blueprint(api_v1, subdomain='api', url_prefix='/v1')

app.register_blueprint(api_v1, url_prefix='/api/v1')
app.register_blueprint(api_v1, subdomain='<user_url_slug', url_prefix='/v1')


@app.route('/')
def index():
    print("===============hell app==============")
    return jsonify(message='hello, world!, app')


if __name__ == "__main__":
    app.run()