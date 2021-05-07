import functools

from flask import Flask, jsonify, request, session

import config
import db_operator

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def ex_handle(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError or TypeError:
            return jsonify({"msg": "WRONG_ARG_FORMAT"})
        except Exception as e:
            return jsonify({"msg": str(e.args)})

    return wrapper


@app.route("/login", methods=["POST"])
@ex_handle
def login():
    data = request.get_json()
    level = db_operator.verify_id_key(data["id"], data["pri_key_sum"])
    if level != -1:
        session["id"] = data["id"]
        return jsonify({"msg": "SUCCESS"})
    else:
        return jsonify({"msg": "用户名或密码不正确"})


@app.route("/register", methods=["POST"])
@ex_handle
def register():
    data = request.get_json()
    db_operator.insert_new_user(data["id"], data["pri_key_sum"])


@app.route("/logout", methods=["GET", "POST"])
@ex_handle
def logout():
    session.pop("id")
    return jsonify({"msg": "SUCCESS"})


@app.route("/verifyuser", methods=["GET", "POST"])
@ex_handle
def verify_user():
    if "id" in session:
        return jsonify({"msg": "SUCCESS"})
    else:
        return jsonify({"msg": "EXPIRED"})
