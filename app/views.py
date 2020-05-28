from datetime import datetime

import pymysql as sql
import requests
from flask import (Blueprint, flash, jsonify, make_response, redirect,
                   render_template, request, session, url_for)

from .api import (api_add_task, api_delete_task, api_user_connect,
                  api_user_create, api_user_disconnect)
from .controller import (create_new_task, create_new_user,
                         delete_selected_task, get_task_info,
                         get_task_list_of_uid, get_user_info, modify_task,
                         sign_in_user)
from .models import (find_uid_with_username, get_task_list,
                     get_task_list_no_uid, task_create, update_task)
from .post_request import (get_uid, make_post_change, make_post_create,
                           make_post_delete, make_post_register,
                           make_post_signin)

blueprint = Blueprint('epytodo', __name__, template_folder="templates",
                      static_folder='static')
# FORMS
@blueprint.route('/forms', methods=['GET'])
def route_forms():
    return render_template("forms.html")


# HOME
@blueprint.route('/', methods=['GET'])
def route_index():
    uid = get_uid()
    array = []
    if uid != -1:
        task_list = get_task_list_of_uid(uid)
        tasks = task_list.get("result")
        tasks_table = tasks.get("task")
        s = 1
        for i in tasks_table:
            list_of_keys = [*i]
            task_dict = i.get(list_of_keys[0])
            task_dict["task_id"] = list_of_keys[0]
            array += [task_dict]
            s += 1
    return render_template("index.html",
                           result=uid,
                           user_id=uid,
                           task_list=array)


# REGISTER POST
@blueprint.route('/register', methods=['POST'])
def route_register():
    if not request.data:
        return {"error": "Missing post request body"}
    data = request.get_json()
    if data is None:
        return {"error": "Missing post json body"}
    username = data.get("username")
    password = data.get("password")
    if username is None:
        return {"error": "Missing 'username' in post body"}
    if password is None:
        return {"error": "Missing 'password' in post body"}
    result = -1
    uid = int(request.cookies.get("user_id", -1))
    if uid != -1:
        return {"error": "Can't register while connected, please sign out"}
    if not username:
        return {"error": "Missing 'username' in post body"}
    if not password:
        return {"error": "Missing 'password' in post body"}
    result = create_new_user(username, password)
    return api_user_create(result)


@blueprint.route('/register/form', methods=['GET'])
def route_register_form_render_template():
    return render_template("register.html")


# REGISTER FORM
@blueprint.route('/register/form', methods=['POST'])
def route_register_form():
    username = request.form.get("username")
    password = request.form.get("password")
    return make_post_register(username, password, get_uid())


# SIGNIN
@blueprint.route('/signin', methods=['POST'])
def route_signin():
    if not request.data:
        return {"error": "Missing post request body"}
    data = request.get_json()
    if data is None:
        return {"error": "Missing post json body"}
    username = data.get("username")
    password = data.get("password")
    if not username:
        return {"error": "Missing 'username' in post body"}
    if not password:
        return {"error": "Missing 'password' in post body"}
    result = -1
    uid = int(request.cookies.get("user_id", -1))
    if uid != -1:
        return {"error": "Can't sign in while connected, please sign out"}
    if username and password:
        result = sign_in_user(username, password)
    resp = make_response(api_user_connect(result))
    if result >= 1:
        resp.set_cookie("user_id", str(result))
        session["user_id"] = result
    return resp


@blueprint.route('/signin/form', methods=['GET'])
def route_signin_form():
    return (render_template("signin.html"))

# SIGNIN FORM
@blueprint.route('/signin/form', methods=['POST'])
def route_signin_form_post():
    username = request.form.get("username")
    password = request.form.get("password")
    result = make_post_signin(username, password, get_uid())
    if result.get("result") == "signin successful":
        session["user_id"] = find_uid_with_username(username)
        return redirect(url_for("epytodo.route_index"))
    return redirect(url_for("epytodo.route_signin_form"))


# SIGNOUT POST
@blueprint.route('/signout', methods=['GET'])
def route_signout_form():
    return render_template("signout.html")


@blueprint.route('/signout', methods=['POST'])
def route_signout_post():
    result = api_user_disconnect()
    session.pop("user_id", None)
    return result

# USER GET
@blueprint.route('/user', methods=['GET'])
def route_user():
    return get_user_info(get_uid())


# USER GET TASK LSIT
@blueprint.route('/user/task', methods=['GET'])
def route_all_user_tasks():
    return get_task_list_of_uid(get_uid())


# GET TASK INFO ID
@blueprint.route('/user/task/<nb>', methods=['GET'])
def route_view_specific_task_get(nb):
    return get_task_info(get_uid(), nb)


# POST ADD TASK
@blueprint.route('/user/task/add', methods=['POST'])
def route_add_task():
    if not request.data:
        return {"error": "Missing post request body"}
    data = request.json
    if data is None:
        return {"error": "Missing post json body"}
    name = data.get("title")
    begin = str(data.get("begin"))
    end = str(data.get("end"))
    status = data.get("status")
    if not name:
        return {"error": "Missing 'title' in post body"}
    if not status:
        return {"error": "Missing 'status' in post body"}
    uid = int(request.cookies.get("user_id", -1))
    if uid == -1:
        return {"error": "you must be logged in"}
    result = create_new_task(name, begin, end, status, uid)
    return api_add_task(uid, result)


# POST CHANGE TASK INFO ID
@blueprint.route('/user/task/<int:nb>', methods=['POST'])
def route_view_specific_task(nb):
    uid = int(request.cookies.get("user_id", -1))
    if uid == -1:
        return ({"error": "you must be logged in"})
    if not request.data:
        return {"error": "Missing post request body"}
    if not request.data:
        return {"error": "Missing post request body"}
    data = request.json
    if data is None:
        return {"error": "Missing post json body"}
    name = data.get("title")
    begin = str(data.get("begin"))
    end = str(data.get("end"))
    status = data.get("status")
    if not name:
        return {"error": "Missing 'title' in post body"}
    if not status:
        return {"error": "Missing 'status' in post body"}
    result = modify_task(nb, name, begin, end, status, uid)
    return result


# POST CHANGE TASK INFO FORM
@blueprint.route('/user/task/change', methods=['GET'])
def route_view_specific_task_form_render():
    return render_template("task.html")


@blueprint.route('/user/task/change', methods=['POST'])
def route_view_specific_task_form():
    nb = request.form.get("task_id")
    name = request.form.get("title")
    begin = str(request.form.get("begin", datetime.now()))
    end = str(request.form.get("end", datetime.now()))
    status = request.form.get("status")
    data_load = {"title": name,
                 "begin": begin,
                 "end": end,
                 "status": status}
    return make_post_change(data_load, nb, get_uid())


# ADD TASK FORM
@blueprint.route('/user/task/add/form', methods=['GET'])
def route_create_new_task_get_render():
    return render_template("add_task.html")


@blueprint.route('/user/task/add/form', methods=['POST'])
def route_create_new_task_get():
    uid = get_uid()
    if uid == -1:
        return api_add_task(uid, 0)
    name = request.form.get("title")
    begin = str(request.form.get("begin"))
    end = str(request.form.get("end"))
    status = request.form.get("status")
    if not begin:
        begin = str(datetime.now())
    if not end:
        end = str(datetime.now())
    return make_post_create(name, begin, end, status, uid)


@blueprint.route('/user/task/delete/<nb>', methods=['GET'])
def route_delete_task_get(nb):
    uid = get_uid()
    if uid == -1:
        return render_template("login_required.html")
    else:
        return render_template("delete_task.html")


@blueprint.route('/user/task/delete/<nb>', methods=['POST'])
def route_delete_task_post(nb):
    make_post_delete(nb)
    return redirect(url_for("epytodo.route_index"))


# DELETE TASK (ID)
@blueprint.route('/user/task/del/<nb>', methods=['POST'])
def route_delete_task(nb):
    uid = int(request.cookies.get("user_id", -1))
    if uid == -1:
        return {"error": "you must be logged in"}
    return api_delete_task(delete_selected_task(nb))


# GRAPHICAL VIEWS
@blueprint.route('/my_tasks', methods=['GET'])
def route_my_tasks():
    uid = get_uid()
    if uid == -1:
        return render_template("login_required.html")
    task_list = get_task_list_of_uid(uid)
    tasks = task_list.get("result")
    tasks_table = tasks.get("task")
    s = 1
    array = []
    for i in tasks_table:
        list_of_keys = [*i]
        task_dict = i.get(list_of_keys[0])
        task_dict["task_id"] = list_of_keys[0]
        array += [task_dict]
        s += 1
    return render_template("my_task.html", task_list=array)


@blueprint.route('/user/task/info/<nb>', methods=['GET'])
def route_task_info(nb):
    uid = get_uid()
    result = get_task_info(uid, nb)
    info = result.get("result")
    return render_template("task_info.html", task_info=info, task_id=nb)
