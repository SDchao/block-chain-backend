import functools
import sqlite3

from flask import Flask, jsonify, request, session

import config
import db_operator
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

        except KeyError:
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


@app.route("/register", methods=["POST"])
@ex_handle
def register():
    data = request.get_json()
    db_operator.insert_new_user(data["id"], data["pri_key_sum"])
    raise SuccessSignal


@app.route("/logout", methods=["GET", "POST"])
@ex_handle
def logout():
    session.pop("id")
    raise SuccessSignal


@app.route("/verifyuser", methods=["GET", "POST"])
@ex_handle
def verify_user():
    if "id" in session:
        raise SuccessSignal({"id": session["id"],
                             "level": session["level"]})
    else:
        raise UserPermissionError


@app.route("/issuecert", methods=["POST"])
@ex_handle
def issue_cert():
    if "level" not in session:
        raise NeedLoginError

    if session["level"] < 1:
        raise UserPermissionError

    data = request.get_json()

    # WIP
    # UPLOAD CODE HERE

    db_operator.insert_new_cert_hash(data["stu_name"], data["cert_id"])
    raise SuccessSignal
