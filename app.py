import base64
import functools
import json
import sqlite3

from flask import Flask, jsonify, request, session

import config
import crypto_operator
import db_operator
import user_manager
from custom_types import NeedLoginError, UserPermissionError, ErrorMessage, SuccessSignal

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def ex_handle(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SuccessSignal as e:
            r = {"msg": "SUCCESS"}
            if e.args:
                d = e.args[0]
                r.update(d)

            return jsonify(r)

        except KeyError or TypeError:
            return jsonify({"msg": "ERR_ARG_FORMAT"})
        except AssertionError:
            return jsonify({"msg": "ERR_ARG_CHECK_FAIL"})
        except ErrorMessage as e:
            if e.args:
                return jsonify({"msg": e.args[0]})
            else:
                return jsonify({"msg": "ERR_UNKNOWN"})
        except UserPermissionError:
            return jsonify({"msg": "权限不足"})
        except NeedLoginError:
            return jsonify({"msg": "需要登录后操作"})
        except sqlite3.Error as e:
            if e.args:
                return jsonify({"msg": f"SQL_ERR_{e.__class__.__name__}", "args": str(e.args)})
            else:
                return jsonify({"msg": f"SQL_ERR_{e.__class__.__name__}"})

    return wrapper


def require_login(ses):
    if "level" not in ses:
        raise NeedLoginError


def require_level(ses, min_level):
    require_login(ses)
    if ses["level"] < min_level:
        raise UserPermissionError


@app.route("/login", methods=["POST"])
@ex_handle
def login():
    data = request.get_json()
    level = db_operator.verify_id_key(data["id"], data["pri_key_sum"])
    if level != -1:
        session["id"] = data["id"]
        session["level"] = level
        raise SuccessSignal
    else:
        raise ErrorMessage("用户名或密码错误")


@app.route("/existuser", methods=["POST"])
@ex_handle
def exist_user():
    exist = user_manager.exist_user(request["id"])

    if exist:
        raise SuccessSignal({"exist": 1})
    else:
        raise SuccessSignal({"exist": 0})


@app.route("/logout", methods=["GET", "POST"])
@ex_handle
def logout():
    session.pop("id")
    session.pop("level")
    raise SuccessSignal


@app.route("/verifyuser", methods=["GET", "POST"])
@ex_handle
def verify_user():
    if "id" in session:
        raise SuccessSignal({"id": session["id"],
                             "level": session["level"]})
    else:
        raise ErrorMessage("EXPIRED")


@app.route("/issuecert", methods=["POST"])
@ex_handle
def issue_cert():
    require_level(session, 2)

    data = request.get_json()

    # DATA CHECK HERE

    stu_id = data["stu_id"]
    # Encrypt data
    if not user_manager.exist_user(stu_id):
        user_manager.register(stu_id)

    data_bytes = json.dumps(data).encode("utf8")
    enc_data = crypto_operator.user_encrypt(stu_id, data_bytes)
    upload_enc_data = base64.b64encode(enc_data)
    print(upload_enc_data)

    conn = db_operator.insert_cert(data["stu_id"], data["cert_id"])
    try:
        # WIP
        # FILE SYS HERE

        # FABRIC HERE

        conn.commit()
    except BaseException as e:
        conn.rollback()
        raise e
    raise SuccessSignal


@app.route("/querycert", methods=["POST"])
@ex_handle
def query_cert():
    data = request.get_json()
    if "cert_id" in data:
        query_cert_public(request)
    else:
        query_cert_self(request)


def get_cert(stu_id: str, cert_id: str):
    # FABRIC HERE
    # FILE SYSTEM HERE
    raw_cert = ''
    enc_cert = base64.b64decode(raw_cert)
    cert = crypto_operator.user_decrypt(stu_id, enc_cert)
    cert_str = cert.decode("utf8")
    cert_json = json.loads(cert_str)
    return cert_json


def query_cert_self(request):
    require_login(session)

    data = request.get_json()
    id = data["stu_id"]

    # Query others' certs
    if id != session["id"]:
        require_level(session, 1)

    cert_id_list = db_operator.find_certs(id)
    res = []
    for cert_id in cert_id_list:
        # cert = get_cert(id, cert_id)
        res.append({"cert_id": cert_id})

    raise SuccessSignal({"certs": res})


def query_cert_public(request):
    data = request.get_json()
    cert_id = data["cert_id"]
    stu_id = data["stu_id"]

    if not db_operator.check_cert_exist(stu_id, cert_id):
        raise ErrorMessage("证书不存在")

    # cert = get_cert(id, cert_id)
    res = [{"cert_id": cert_id}]

    raise SuccessSignal({"certs": res})


@app.route("/modifycert", methods=["POST"])
@ex_handle
def modify_cert():
    require_level(session, 2)

    data = request.get_json()
    stu_id = data["stu_id"]
    cert_id = data["cert_id"]

    if not db_operator.check_cert_exist(stu_id, cert_id):
        raise ErrorMessage("证书不存在")
    # FILE SYSTEM HERE
    # FABRIC HERE

    raise SuccessSignal


if __name__ == '__main__':
    app.run()
