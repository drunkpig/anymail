import logging, json, datetime
from logging.config import fileConfig
import sqlite3,os
import mimetypes
import base64
from flask import abort
from flask import make_response
import mailparser
from flask import Flask, jsonify, redirect, url_for
from flask import request
from flask import render_template
from urllib.parse import quote

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # json显示中文
# fileConfig("logging.ini")
# logger = logging.getLogger()

DB = os.path.expanduser("~/mailbox/fake_mail.db")
TABLE = "fake_mail"


@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    sql = f"""
                select id, email_title, email_from, email_to, dt, has_attach from {TABLE}  order by dt desc limit 100
            """
    cur.execute(sql)
    val = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", mails=val)


@app.route('/detail/<int:id>/<type>', methods=['GET'])
def detail(id, type):
    """

    :param id:
    :param type:
    :return:
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    sql = f"""
                    select id, dt, email_raw from {TABLE}  where id={id}
                """
    cur.execute(sql)
    val = cur.fetchone()
    cur.close()
    conn.close()
    raw_email = val[2]
    mail = mailparser.parse_from_string(raw_email)
    if type=='html':
        mail_content = mail.text_html
    else:
        mail_content = mail.text_plain
    from_ = mail.from_[0][1]
    to_ = mail.to[0][1]
    dt = val[1]
    email_subject = mail.subject
    return render_template("detail.html", **{"title":email_subject, "from":from_, "type":type, "to":to_, "dt":dt, "mail_content":mail_content,
                                             "attachements":mail.attachments, "mid":id
                                             })


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    sql = f"""
                    delete from {TABLE} where id = {id}
                """
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    return redirect("/")


@app.route('/email/<path:email>', methods=['GET'])
def email(email):
    """
    获得时间最近的一个email
    :param email:
    :param type:
    :return:
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    sql = f"""
                        select id,dt,email_raw from {TABLE}  where email_to=? order by dt desc limit 1;
                    """
    cur.execute(sql, [email])
    val = cur.fetchone()
    cur.close()
    conn.close()
    raw_email = val[2]
    mail = mailparser.parse_from_string(raw_email)
    result = {}
    result['id'] = val[0]
    result['from'] = mail.from_[0][1]
    result['to_'] = mail.to[0][1]
    result['title'] = mail.subject
    result['dt'] = val[1]
    result['html'] = mail.text_html
    result['text'] = mail.text_plain
    return jsonify(result)


@app.route('/attach/<int:email_id>/<file_name>', methods=['GET'])
def attach(email_id, file_name):
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        sql = f"""
                            select email_raw from {TABLE}  where id={email_id}
                        """
        cur.execute(sql)
        val = cur.fetchone()
        cur.close()
        conn.close()
        raw_email = val[0]
        mail = mailparser.parse_from_string(raw_email)
        data = ""
        charset = "utf-8"
        for att in mail.attachments:
            fnm =att['filename']
            if fnm==file_name:
                data = att['payload']
                charset = "utf-8" if att['charset'] is None else att['charset']
                data = base64.b64decode(data)
        response = make_response(data)
        mime_type = mimetypes.guess_type(file_name)[0]
        response.headers['Content-Type'] = mime_type
        response.headers['Content-Disposition'] = f'attachment; "filename*=UTF-8 {quote(file_name.encode("utf-8"))}'
        return response
    except Exception as err:
        print(err)
        abort(404)


def start_web(host, port):
    app.run(host, port)


if __name__=="__main__":
    app.run("0.0.0.0", "8888", debug=True)
