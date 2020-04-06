from app import app
from flask import render_template, request, redirect, url_for
from flask import jsonify, flash
import pymysql as sql
from config import *
from .models import create_new_user, delete_task, create_new_task
from .models import sign_in_user, get_user_info
from app import login_only, not_login_only
from datetime import datetime


def api_user_create(username, password, return_code):
    result = {}
    if return_code == -1 or not username.isalnum():
        result['error'] = "internal error"
    elif (return_code == 0):
        result['error'] = "account already exists"
    else:
        result['result'] = "account created"
    return (result)


def api_user_connect(username, password, return_code, user_id):
    result = {}
    if return_code == -1 or user_id == -2:
        result['error'] = "internal error"
    elif (return_code == 0):
        result['error'] = "login or password does not match"
    elif (return_code == 1):
        result['result'] = "signin successful"
    return (result)


def api_user_disconnect():
    result = {}
    if (app.id == -1):
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


def api_delete_task(number, user_id, return_code):
    result = {}
    if (user_id == -1):
        result['error'] = "you must be logged in"
        return result
    if (return_code == 0):
        result['error'] = "task id does not exist"
        return result
    result['result'] = "task deleted"
    return result
