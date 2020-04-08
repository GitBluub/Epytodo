from datetime import datetime

import pymysql as sql
from flask import (flash, jsonify, redirect, render_template, request, session,
                   url_for)


def api_user_create(username, password, return_code):
    if return_code == -1 or not username.isalnum():
        return {"error": "internal error"}
    elif (return_code == 0):
        return {"error": "account already exists"}
    else:
        return {"result": "account created"}


def api_user_connect(username, password, return_code):
    if return_code == -1:
        return {"error": "internal error"}
    elif (return_code == 0):
        return {"error": "login or password does not match"}
    elif (return_code >= 1):
        return {"result": "signin successful"}


def api_user_disconnect():
    if not session.get("user_id"):
        return {"error": "internal error"}
    else:
        return {"result": "signout successful"}


def api_add_task(user_id, name, return_code):
    if (user_id == -1):
        return {"error": "you must be logged in"}
    if not name:
        return {"error": "internal error"}
    if return_code == 0:
        return {"error": "internal error"}
    return {"result": "new task added"}


def api_delete_task(return_code):
    if (return_code == 0):
        return {"error": "task id does not exist"}
    return {"result": "task deleted"}
