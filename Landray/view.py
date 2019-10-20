from flask import Blueprint, render_template
from Landray.api import Open

bp = Blueprint("test", __name__)


@bp.route("/test")
def hello():
    return "index, World!"


@bp.route("/")
def index():
    body = {
        "authModes": [],
        "returnUrl": "http://return_url_ente/test",
        "customTag": "test_customTag_by_yz",
        "notifyUrl": "http://notify_url_ente/test"
    }
    obj = Open()
    action_url = obj.create_enterprise_authentications(body)
    if action_url is False:
        return "请求出错"
    return render_template('index.html', action_url=action_url)
