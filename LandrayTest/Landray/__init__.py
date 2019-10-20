import logging

from flask import Flask

"""Create and configure an instance of the Flask application."""
app = Flask(__name__, instance_relative_config=True)
handler = logging.FileHandler('log.log', encoding='UTF-8')

handler.setLevel(logging.DEBUG)

logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

handler.setFormatter(logging_format)

app.logger.addHandler(handler)
"""
配置文件 instance 管理
"""
app.config.from_pyfile("config.py")

app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY="dev",
    DEBUG=True
)

from Landray.view import bp

app.register_blueprint(bp)


@app.route("/hello")
def hello():
    return "Hello, World!"
