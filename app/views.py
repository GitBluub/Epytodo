from datetime import datetime

import pymysql as sql
import requests
from flask import (flash, jsonify, make_response, redirect, render_template,
                   request, session, url_for)

from app import app

from .api import (api_add_task, api_delete_task, api_user_connect,
                  api_user_create, api_user_disconnect)
from .controller import (create_new_task, create_new_user,
                         delete_selected_task, get_task_info,
                         get_task_list_of_uid, get_user_info, modify_task,
                         sign_in_user)
from .models import (find_uid_with_username, get_task_list,
                     get_task_list_no_uid, task_create, update_task)
from .post_request import (get_uid, make_post_change, make_post_create,
                           make_post_register, make_post_signin)


# FORMS
@app.route('/forms', methods=['GET'])
def route_forms():
    return (render_template("forms.html"))


# HOME
@app.route('/', methods=['GET'])
def route_index():
    uid = get_uid()
    return render_template("index.html", result=uid, user_id=uid)


# REGISTER POST
@app.route('/register', methods=['POST'])
def route_register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    result = -1
    if username and password:
        # NOTE: See api.py
        result = create_new_user(username, password)
    # TODO: Returning the following format:
    #       jsonify(...), integer
    #       allows to leverage HTTP codes.
    # NOTE: Example:
    #       {"error": True, "message": "user %username already exists"}, 422
    return (jsonify(api_user_create(username, password, result)))


@app.route('/register/form', methods=['GET'])
def route_register_form_render_template():
    return (render_template("register.html"))


# REGISTER FORM
@app.route('/register/form', methods=['POST'])
def route_register_form():
    # TODO: It might be a bit less risky to use `request.form.get`
    #       and check if either username and password are None
    #       -> Current code could induce KeyError
    username = request.form["username"]
    password = request.form["password"]
    return make_post_register(username, password)


# SIGNIN
@app.route('/signin', methods=['POST'])
def route_signin():
    if not request.data:
        # TODO: This return could return a more meaningful error message
        #       such as "Missing post data" with a "Invalid request" HTTP code.
        return {"error": "internal error"}
    data = request.get_json()
    if data is None:
        return {"error": "internal error"}
    username = data.get("username")
    password = data.get("password")
    result = -1
    if request.cookies.get("user_id") is not None:
        return (jsonify(api_user_connect(username, password, result)))
    if username and password:
        result = sign_in_user(username, password)
    resp = make_response(
        jsonify(api_user_connect(username, password, result)))
    if result != -1:
        session["user_id"] = result
    return resp


@app.route('/signin/form', methods=['GET'])
def route_signin_form():
    return (render_template("signin.html"))

# SIGNIN FORM
@app.route('/signin/form', methods=['POST'])
def route_signin_form_post():
    username = request.form["username"]
    password = request.form["password"]
    uid = session.get("user_id")
    result = make_post_signin(username, password, uid)
    if result.get("result") == "signin successful":
        session["user_id"] = find_uid_with_username(username)
    return result


# SIGNOUT POST
@app.route('/signout', methods=['GET'])
def route_signout_form():
    return render_template("signout.html")


@app.route('/signout', methods=['POST'])
def route_signout_post():
    result = jsonify(api_user_disconnect())
    session.pop("user_id", None)
    return result

# USER GET
@app.route('/user', methods=['GET'])
def route_user():
    return jsonify(get_user_info(get_uid()))


# USER GET TASK LSIT
@app.route('/user/task', methods=['GET'])
def route_all_user_tasks():
    return jsonify(get_task_list_of_uid(get_uid()))


# GET TASK INFO ID
@app.route('/user/task/<nb>', methods=['GET'])
def route_view_specific_task_get(nb):
    return jsonify(get_task_info(get_uid(), nb))


# POST CHANGE TASK INFO ID
@app.route('/user/task/<nb>', methods=['POST'])
def route_view_specific_task(nb):
    data = request.get_json()
    if get_uid() == -1:
        return ({"error": "you must be logged in"})
    if data is None:
        return {"error": "internal error"}
    result = modify_task(nb, data)
    return jsonify(result)


# POST CHANGE TASK INFO FORM
@app.route('/user/task/change', methods=['GET'])
def route_view_specific_task_form_render():
    return (render_template("task.html"))


@app.route('/user/task/change', methods=['POST'])
def route_view_specific_task_form():
    # TODO: Use get instead of __getattr__
    # TODO: Use PUT instead of POST (POST = creation, PUT = edition)
    nb = request.form["task_id"]
    name = request.form["title"]
    begin = request.form["begin"]
    end = request.form["end"]
    status = request.form["status"]
    data_load = {"title": name,
                 "begin": begin,
                 "end": end,
                 "status": status}
    return make_post_change(data_load, nb)


# POST ADD TASK
@app.route('/user/task/add', methods=['POST'])
def route_add_task():
    data = request.json
    name = data.get("title")
    begin = data.get("begin")
    end = data.get("end")
    status = data.get("status")
    if not name:
        return jsonify(api_add_task(get_uid(), name, 0))
    result = create_new_task(name, begin, end, status)
    return jsonify(api_add_task(get_uid(), name, result))


# ADD TASK FORM
@app.route('/user/task/add/form', methods=['GET'])
def route_create_new_task_get_render():
    return (render_template("add_task.html"))


@app.route('/user/task/add/form', methods=['POST'])
def route_create_new_task_get():
    if get_uid() == -1:
        return jsonify(api_add_task(get_uid(), "", 0))
    name = request.form["title"]
    begin = request.form["begin"]
    end = request.form["end"]
    status = request.form["status"]
    if not begin:
        begin = datetime.now()
    if not end:
        end = datetime.now()
    return make_post_create(name, begin, end, status)


# DELETE TASK (ID)
@app.route('/user/task/del/<nb>', methods=['GET', 'POST'])
def route_delete_task(nb):
    if get_uid() == -1:
        return {"error": "you must be logged in"}
    return jsonify(api_delete_task(delete_selected_task(nb)))
