from datetime import datetime

import pymysql as sql
from flask import (flash, jsonify, redirect, render_template, request, session,
                   url_for)


def api_user_create(return_code):
    if return_code == -1:
        return {"error": "internal error"}
    if return_code == "account already exists":
        return {"error": "account already exists"}
    else:
        return {"result": "account created"}


def api_user_connect(return_code):
    if return_code == -1:
        return {"error": "internal error"}
    if return_code == 0:
        return {"error": "login or password does not match"}
    if return_code >= 1:
        return {"result": "signin successful"}
    return {"error": "internal error"}


def api_user_disconnect():
    if not session.get("user_id"):
        return {"error": "internal error"}
    else:
        return {"result": "signout successful"}


def api_add_task(user_id, return_code):
    if user_id == -1:
        return {"error": "you must be logged in"}
    if return_code == 0:
        return {"error": "invalid connection, please reconnect"}
    if return_code == -1:
        return {"error": "task with same name already exists"}
    return {"result": "new task added"}


def api_delete_task(return_code):
    if (return_code == 0):
        return {"error": "task id does not exist"}
    return {"result": "task deleted"}
