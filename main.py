from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from filter import DFAFilter
from flask_pymongo import PyMongo
from flask_wtf import CSRFProtect
import requests
import re
from Crypto.Cipher import AES
from bson.objectid import ObjectId

app = Flask(__name__)
gfw = DFAFilter()
gfw.parse("keywords")

app.secret_key = "\x18\xc0\xe6\xa4V\x84G\xb9o\xb8\xbf2\xa4\xd9\xcb_\xff\xa2\xfe\xa9l\xd8\t\xc9"
CSRFProtect(app)
mongo = PyMongo(app, uri="mongodb://localhost:27017/stuguide")

test_account = {"test01": "1234567890"}


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
    f = mongo.db.collection.find({}, {
        "_id": 0,
        "text": 1,
        "icon": 1,
        "color": 1
    }).sort([("_id", -1)]).limit(50)
    result = [x for x in f]
    return jsonify(result)


@app.route("/danmu/send/", methods=["POST"], endpoint="send_danmu")
@login_required
def send_danmu():
    txt = str(request.form.get("text", ""))
    icon = str(request.form.get("icon", ""))
    color = str(request.form.get("color", ""))
    studentid = session.get("studentid", "")
    if mongo.db.banuser.find_one({"studentid": studentid}) != None:
        return jsonify({"status": -2})
    txt = re.sub(r"<[^>]+>", "", txt, flags=re.S)
    if txt != "" and icon != "" and color != "" and icon.isdigit():
        icon = int(icon)
        if 0 < len(txt) < 40 and icon in [0, 1]:
            filtered, result = gfw.filter(txt)
            if result == False:
                mongo.db.collection.insert_one({
                    "text": txt,
                    "icon": icon,
                    "color": color,
                    "studentid": studentid
                })
                return jsonify({"status": 1, "text": txt, "filter": False})
            else:
                return jsonify({"status": 1, "text": filtered, "filter": True})
    return jsonify({"status": 0})


@app.route("/danmu/login/", methods=["POST"], endpoint="login_danmu")
def login_danmu():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    captchacode = request.form.get("captchacode", "")
    captchavalue = request.form.get("captchavalue", "")
    if username != "" and password != "":
        if username in test_account.keys():
            if test_account.get(username, "") == password:
                result = {"status": 0}
        else:
            result = login_yunxiao(username, password, captchacode,
                                   captchavalue)
        if result["status"] == 0:
            session["loggedin"] = True
            session["studentid"] = username
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
        studentid = Aes_ECB(splitted[0]).AES_decrypt(splitted[1])
        session["loggedin"] = True
        session["studentid"] = studentid
        adm = mongo.db.adminuser.find_one({"username": studentid}, {
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
    return render_template("manage.html",
                           admin_name=session.get("admin_name", "NULL"))


@app.route("/danmu/super-admin/get/", endpoint="get_manage")
@admin_required
def get_manage():
    f = mongo.db.collection.find({}, {
        "_id": 1,
        "text": 1,
        "studentid": 1
    }).sort([("_id", -1)]).limit(50)
    result = []
    for x in f:
        result.append({
            "_id": str(x["_id"]),
            "text": x.get("text", ""),
            "studentid": x.get("studentid", "")
        })
    return jsonify(result)


@app.route("/danmu/super-admin/delete/",
           methods=["POST"],
           endpoint="delete_manage")
@admin_required
def delete_manage():
    if mongo.db.banuser.find({
            "studentid": session.get("studentid", "")
    }).count() > 0:
        return jsonify({"status": 0})
    node_id = request.form.get("id", "")
    if node_id == "":
        return jsonify({"status": 0})
    result = mongo.db.collection.remove({"_id": ObjectId(node_id)})
    if result["n"] == 1:
        return jsonify({"status": 1})
    else:
        return jsonify({"status": 0})


@app.route("/danmu/super-admin/banuser/",
           methods=["POST"],
           endpoint="banuser_manage")
@admin_required
def banuser_manage():
    if mongo.db.banuser.find({
            "studentid": session.get("studentid", "")
    }).count() > 0:
        return jsonify({"status": 0})
    node_id = request.form.get("studentid", "")
    if node_id == "":
        return jsonify({"status": 0})
    result = mongo.db.banuser.update(
        {"studentid": node_id},
        {"$setOnInsert": {
            "operator": session.get("admin_name", "")
        }},
        upsert=True)
    if result["n"] == 1:
        return jsonify({"status": 1})
    else:
        return jsonify({"status": 0})


@app.route("/danmu/super-admin/recoveruser/",
           methods=["POST"],
           endpoint="recoveruser_manage")
@admin_required
def recoveruser_manage():
    if mongo.db.banuser.find({
            "studentid": session.get("studentid", "")
    }).count() > 0:
        return jsonify({"status": 0})
    node_id = request.form.get("studentid", "")
    if node_id == "":
        return jsonify({"status": 0})
    result = mongo.db.banuser.remove({"studentid": node_id})
    if result["n"] == 1:
        return jsonify({"status": 1})
    else:
        return jsonify({"status": 0})


@app.route("/danmu/super-admin/getbanneduser/",
           endpoint="getbanneduser_manage")
@admin_required
def getbanneduser_manage():
    result = mongo.db.banuser.find({}, {
        "_id": 0,
        "studentid": 1,
        "operator": 1
    }).sort([("_id", -1)]).limit(50)
    pres = [x for x in result]
    return jsonify(pres)


if __name__ == "__main__":
    # 请务必使用gunicorn+gevent启动，此处为debug
    app.run(host="0.0.0.0", port=80, debug=True)
