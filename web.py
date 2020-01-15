import logging, json, datetime
from logging.config import fileConfig

from flask import Flask,jsonify
from flask import request

app = Flask(__name__)
# fileConfig("logging.ini")
# logger = logging.getLogger()


@app.route('/index', methods=['GET'])
def index():
    return jsonify({"code":"success"})


@app.route('/list', methods=['GET'])
def list():
    pass


@app.route('/detail', methods=['GET'])
def detail():
    pass


@app.route('/delete', methods=['GET'])
def delete():
    pass


@app.route('/email/{email}/{type}', methods=['GET'])
def email():
    pass


def start_web(host, port):
    app.run(host, port)


if __name__=="__main__":
    app.run("0.0.0.0", "8888")
