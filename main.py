from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_wtf import CSRFProtect
import requests
import re
import socket
from Crypto.Cipher import AES
from bson.objectid import ObjectId
import random

app = Flask(__name__)

app.config["SECRET_KEY"] = "\x18\xc0\xe6\xa4V\x84G\xb9o\xb8\xbf2\xa4\xd9\xcb_\xff\xa2\xfe\xa9l\xd8\t\xc9"

test_account = {"test01": "1234567890"}
HOST = "0.0.0.0"
PORT = 80
DEBUG = True

if socket.gethostname().find("HCC") != -1:
    app.config["SERVER_NAME"] = "guide.hcc.io"
    HOST = "127.0.0.1"
    PORT = 5500
    test_account = {}
    DEBUG = False

CSRFProtect(app)
mongo = PyMongo(app, uri="mongodb://localhost:27017/stuguide")
verifier_count = 5

class Aes_ECB(object):
    def __init__(self, key):
        self.key = key
        self.MODE = AES.MODE_ECB
        self.BS = AES.block_size
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def add_to_16(self, value):
        return str.encode(value)

    def AES_decrypt(self, text):
        aes = AES.new(self.add_to_16(self.key), self.MODE)
        hex_decrypted = bytes.fromhex(text)
        decrypted_text = self.unpad(aes.decrypt(hex_decrypted).decode('utf-8'))
        decrypted_code = decrypted_text.rstrip('\0')
        return decrypted_code


def login_yunxiao(username, password, captchaCode='', captchaValue=''):
    reqheaders = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'account.yunxiao.com',
        'Referer':
        'https://account.yunxiao.com/partner?service=http://bnds.idsp.yunxiao.com/Portal/LayoutD/CasLogin.aspx?ax=1',
        'User-Agent':
        'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    dict_edit = {
        'status': 0,
        'name': '',
        'captchaCode': '',
    }
    data = {
        'loginName': username,
        'password': password,
        'domain': 'bnds',
        'captchaCode': captchaCode,
        'captchaValue': captchaValue,
        'rememberMe': 'false',
        'service':
        'http://bnds.idsp.yunxiao.com/Portal/LayoutD/CasLogin.aspx?ax'
    }
    responseData = requests.post("https://account.yunxiao.com/",
                                 data=data,
                                 headers=reqheaders).json()
    if 'errCode' in responseData.keys():
        dict_edit['status'] = responseData['errCode']
        dict_edit['name'] = responseData['errMsg']
        dict_edit['captchaCode'] = ''
        if 'captchaCode' in responseData.keys():
            dict_edit['captchaCode'] = responseData['captchaCode']
    return dict_edit


def login_required(func):
    def inner(*args, **kwargs):
        if not session.get("loggedin", False):
            return redirect(url_for("layout_danmu"))
        return func(*args, **kwargs)
    return inner


def admin_required(func):
    def inner(*args, **kwargs):
        if not session.get("admin_loggedin", False):
            return redirect(url_for("layout_danmu"))
        return func(*args, **kwargs)
    return inner


def banned_checked(func):
    def inner(*args, **kwargs):
        if mongo.db.banuser.find_one({"username": session.get("username", "")}) != None:
            return jsonify({"status": 0})
        return func(*args, **kwargs)
    return inner


@app.route("/", endpoint="layout_homeredirect")
def layout_homeredirect():
    return redirect(url_for("layout_daka"))


@app.route("/daka/", endpoint="layout_daka")
def layout_daka():
    return render_template("daka.html")


@app.route("/gallery/", endpoint="layout_gallery")
def layout_gallery():
    return render_template("gallery.html")


@app.route("/about/", endpoint="layout_about")
def layout_about():
    return render_template("about.html")


@app.route("/tos/", endpoint="layout_tos")
def layout_tos():
    return render_template("tos.html")


@app.route("/danmu/", endpoint="layout_danmu")
def layout_danmu():
    if session.get("loggedin", False) == True:
        if session.get("admin_loggedin", False) == False:
            return render_template("danmu.html",
                                   loggedin="true",
                                   hide_admin="display:none;")
        else:
            return render_template("danmu.html",
                                   loggedin="true",
                                   hide_admin="")
    return render_template("danmu.html",
                           loggedin="false",
                           hide_admin="display:none;")

@app.route("/danmu/get/", endpoint="get_danmu")
@login_required
def get_danmu():
    f = mongo.db.collection.find({
        "verified": 1
    }, {
        "_id": 0,
        "text": 1,
        "icon": 1,
        "color": 1
    }).sort([("_id", -1)]).limit(40)
    result = [x for x in f]
    return jsonify(result)


@app.route("/danmu/send/", methods=["POST"], endpoint="send_danmu")
@login_required
def send_danmu():
    txt = str(request.form.get("text", ""))
    icon = str(request.form.get("icon", ""))
    color = str(request.form.get("color", ""))
    username = session.get("username", "")
    if mongo.db.banuser.find_one({"username": username}) != None:
        return jsonify({"status": -2})
    txt = re.sub(r"<[^>]+>", "", txt, flags=re.S)
    if txt != "" and icon != "" and color != "" and icon.isdigit():
        icon = int(icon)
        if 0 < len(txt) < 40 and icon in [0, 1]:
            mongo.db.collection.insert_one({
                "text": txt,
                "icon": icon,
                "color": color,
                "username": username,
                "verified": 0,
                "verifier": random.randint(1, verifier_count)
            })
            return jsonify({"status": 1, "text": txt})
    return jsonify({"status": 0})


@app.route("/danmu/login/", methods=["POST"], endpoint="login_danmu")
def login_danmu():
    username = str(request.form.get("username", ""))
    password = str(request.form.get("password", ""))
    captchacode = request.form.get("captchacode", "")
    captchavalue = request.form.get("captchavalue", "")
    if username != "" and password != "":
        if username in test_account.keys():
            if test_account.get(username, "") == password:
                result = {"status": 0}
            else:
                result = {"status": -1}
        else:
            result = login_yunxiao(username, password, captchacode,
                                   captchavalue)
        if result["status"] == 0:
            session["loggedin"] = True
            session["username"] = username
            adm = mongo.db.adminuser.find_one({"username": username}, {
                "_id": 0,
                "name": 1
            })
            if adm != None:
                session["admin_loggedin"] = True
                session["admin_name"] = adm.get("name", "")
                return jsonify({"status": 0, "is_admin": 1})
            else:
                session["admin_loggedin"] = False
                return jsonify({"status": 0, "is_admin": 0})
        elif result["status"] == -1:
            return jsonify({"status": -1})
        elif result["status"] == -2:
            return jsonify({
                "status": -2,
                "captchacode": result.get("captchaCode", "")
            })
        elif result["status"] == -3:
            return jsonify({"status": -3})
        elif result["status"] == 3:
            return jsonify({"status": 3})
        else:
            return jsonify({"status": -4})
    return jsonify({"status": -4})


@app.route("/danmu/external_login/", endpoint="external_login_danmu")
def external_login_danmu():
    param = request.args.get("param", "")
    if param == "":
        return jsonify({"status": 0, "msg": "param error"})
    splitted = param.split("[-]")
    if len(splitted) != 2:
        return jsonify({"status": 0, "msg": "param error"})
    try:
        username = str(Aes_ECB(splitted[0]).AES_decrypt(splitted[1]))
        session["loggedin"] = True
        session["username"] = username
        adm = mongo.db.adminuser.find_one({"username": username}, {
            "_id": 0,
            "name": 1
        })
        if adm != None:
            session["admin_loggedin"] = True
            session["admin_name"] = adm.get("name", "")
        else:
            session["admin_loggedin"] = False
        return redirect(url_for("layout_danmu"))
    except:
        return jsonify({"status": 0, "msg": "param error"})


@app.route("/danmu/logout/", endpoint="logout_danmu")
def logout_danmu():
    session.clear()
    return redirect(url_for("layout_danmu"))


@app.route("/danmu/super-admin/", endpoint="layout_manage")
@admin_required
def layout_manage():
    return render_template("manage.html", admin_name=session.get("admin_name", "NULL"), verifier_count=verifier_count)


@app.route("/danmu/super-admin/get/", endpoint="get_manage")
@admin_required
def get_manage():
    f = mongo.db.collection.find({"verified": 0, "verifier": int(request.args.get("verifier", 1))}, {
        "_id": 1,
        "text": 1,
        "username": 1
    }).sort([("_id", -1)]).limit(8)
    result = []
    for x in f:
        result.append({
            "_id": str(x["_id"]),
            "text": x.get("text", ""),
            "username": x.get("username", "")
        })
    return jsonify(result)


@app.route("/danmu/super-admin/operation/", methods=["POST"], endpoint="operation_manage")
@admin_required
@banned_checked
def operation_manage():
    accept_id = request.form.getlist("accept_id[]")
    delete_id = request.form.getlist("delete_id[]")
    accept_list = [ObjectId(x) for x in accept_id]
    delete_list = [ObjectId(x) for x in delete_id]
    mongo.db.collection.update_many({"_id": {"$in": accept_list}}, {
                               "$set": {"verified": 1}})
    mongo.db.collection.remove({"_id": {"$in": delete_list}})
    return jsonify({"status": 1})


@app.route("/danmu/super-admin/banuser/", methods=["POST"], endpoint="banuser_manage")
@admin_required
@banned_checked
def banuser_manage():
    node_id = request.form.get("username", "")
    if node_id == "":
        return jsonify({"status": 0})
    result = mongo.db.banuser.update(
        {"username": node_id},
        {"$setOnInsert": {
            "operator": session.get("admin_name", "")
        }},
        upsert=True)
    if result["n"] == 1:
        return jsonify({"status": 1})
    else:
        return jsonify({"status": 0})


@app.route("/danmu/super-admin/recoveruser/", methods=["POST"], endpoint="recoveruser_manage")
@admin_required
@banned_checked
def recoveruser_manage():
    if mongo.db.banuser.find({
            "username": session.get("username", "")
    }).count() > 0:
        return jsonify({"status": 0})
    node_id = request.form.get("username", "")
    if node_id == "":
        return jsonify({"status": 0})
    result = mongo.db.banuser.remove({"username": node_id})
    if result["n"] == 1:
        return jsonify({"status": 1})
    else:
        return jsonify({"status": 0})


@app.route("/danmu/super-admin/getbanneduser/", endpoint="getbanneduser_manage")
@admin_required
def getbanneduser_manage():
    result = mongo.db.banuser.find({}, {
        "_id": 0,
        "username": 1,
        "operator": 1
    }).sort([("_id", -1)]).limit(50)
    pres = [x for x in result]
    return jsonify(pres)


if __name__ == "__main__":
    # 请务必使用gunicorn+gevent启动，此处为debug
    app.run(host=HOST, port=PORT, debug=DEBUG)
