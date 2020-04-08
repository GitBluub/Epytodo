from datetime import datetime

import pymysql as sql
from flask import (flash, jsonify, redirect, render_template, request, session,
                   url_for)

from app import app


# NOTE: Instead of returning a jsonified single-entry dict
#       the format described below would bring a bit of consistency
#       in your HTTP return statemetns:

"""
.. code:javascript
    {
        "error": true, // false
        "message": "account created", // "missing name,password"
    }
"""

def api_user_create(username, password, return_code):
    result = {}
    if return_code == -1 or not username.isalnum():
        result['error'] = "internal error"
    elif (return_code == 0):
        result['error'] = "account already exists"
    else:
        result['result'] = "account created"
    return (result)


def api_user_connect(username, password, return_code):
    result = {}
    if return_code == -1:
        result['error'] = "internal error"
    elif (return_code == 0):
        result['error'] = "login or password does not match"
    elif (return_code >= 1):
        result['result'] = "signin successful"
    return (result)


def api_user_disconnect():
    result = {}
    if not session.get("user_id"):
        result['error'] = "internal error"
    else:
        result['result'] = "signout successful"
    return (result)


def api_add_task(user_id, name, return_code):
    result = {}
    if (user_id == -1):
        result['error'] = "you must be logged in"
        return result
    if not name:
        result['error'] = "internal error"
        return result
    if return_code == 0:
        result['error'] = "internal error"
        return result
    result['result'] = "new task added"
    return result


def api_delete_task(return_code):
    result = {}
    if (return_code == 0):
        result['error'] = "task id does not exist"
        return result
    result['result'] = "task deleted"
    return result
