from app import app
from flask import render_template, request, redirect, url_for
from flask import jsonify, flash
import pymysql as sql
from config import *
from .models import *
from app import login_only, not_login_only
from datetime import datetime
from .api import *
import requests
from .controller import modify_task

#######FORMS
@app.route('/forms', methods=['GET'])
def route_forms():
    return (render_template("forms.html"))

#######HOME
@app.route('/', methods=['GET'])
def route_index():
    return (render_template("index.html", result=app.id, user_id=app.id))

#######REGISTER POST
@app.route('/register', methods=['POST'])
def route_register():
    data = request.json
    print(data)
    username = data.get("username")
    password = data.get("password")
    result = -1
    if username == None or password == None:
        result = -1
    elif len(username) and len(password):
        result = create_new_user(username, password)
    return (jsonify(api_user_create(username, password, result)))

#######REGISTER FORM
@app.route('/register/form', methods=['GET', 'POST'])
def route_register_form():
    if request.method == 'GET':
        return (render_template("register.html"))
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data_load = {"username":username,
                    "password":password}
        r = requests.post(f'http://127.0.0.1:5000/register',
                            json = data_load,
                            headers = headers)
        return (r.json())

#######SIGNIN
@app.route('/signin', methods=['POST'])
def route_signin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    result = -1
    if (app.id != -1):
        return (jsonify(api_user_connect(username, password, result, -2)))
    if len(username) and len(password):
        result = sign_in_user(username, password)
    return (jsonify(api_user_connect(username, password, result, app.id)))

#######SIGNIN FORM
@app.route('/signin/form', methods=['GET', 'POST'])
def route_signin_form():
    if request.method == 'GET':
        return (render_template("signin.html"))
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data_load = {"username":username,
                    "password":password}
        r = requests.post(f'http://127.0.0.1:5000/signin',
                            json = data_load,
                            headers = headers)
        return (r.json())

#######SIGNOUT POST
@app.route('/signout', methods=['GET'])
def route_signout():
    t = jsonify(api_user_disconnect())
    app.id = -1
    return t

#######USER GET
@app.route('/user', methods=['GET'])
def route_user():
    return (jsonify(get_user_info(app.id)))

#######USER GET TASK LSIT
@app.route('/user/task', methods=['GET'])
def route_all_user_tasks():
    return (jsonify(get_task_list(app.id)))

#######GET TASK INFO ID
@app.route('/user/task/<nb>', methods=['GET'])
def route_view_specific_task_get(nb):
    if request.method == "GET":
        return (jsonify(get_task_info(app.id, nb)))

#######POST CHANGE TASK INFO ID
@app.route('/user/task/<nb>', methods=['POST'])
def route_view_specific_task(nb):
    data = request.get_json()
    if app.id == -1:
        return ({"error":"you must be logged in"})
    internal_error = {"error" : "internal error"}
    if data == None:
        return (internal_error)
    result = modify_task(nb, data)
    return (jsonify(result))

#######POST CHANGE TASK INFO FORM
@app.route('/user/task/change', methods=['GET', 'POST'])
def route_view_specific_task_form():
    if request.method == "GET":
        return (render_template("task.html"))
    if request.method == "POST":
        nb = request.form["task_id"]
        name = request.form["title"]
        begin = request.form["begin"]
        end = request.form["end"]
        status = request.form["status"]
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data_load = {"title":name,
                    "begin":begin,
                    "end":end,
                    "status":status}
        r = requests.post(f'http://127.0.0.1:5000/user/task/{nb}',
                            json = data_load,
                            headers = headers)
        return (r.json())

#######POST ADD TASK
@app.route('/user/task/add', methods=['POST'])
def route_add_task():
    data = request.json
    name = data.get("title")
    begin = data.get("begin")
    end = data.get("end")
    status = data.get("status")
    if not name:
        return jsonify(api_add_task(app.id, name, 0))
    result = create_new_task(name, begin, end, status)
    return jsonify(api_add_task(app.id, name, result))

#######ADD TASK FORM
@app.route('/user/task/add/form', methods=['GET', 'POST'])
def route_create_new_task_get():
    if request.method == 'GET':
        return (render_template("add_task.html"))
    if request.method == 'POST':
        if app.id == -1:
            return jsonify(api_add_task(app.id, "", 0))
        name = request.form["title"]
        begin = request.form["begin"]
        end = request.form["end"]
        status = request.form["status"]
        if not begin:
            begin = datetime.now()
        if not end:
            end = datetime.now()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data_load = {"title":name,
                    "begin":begin,
                    "end":end,
                    "status":status}
        r = requests.post(f'http://127.0.0.1:5000/user/task/add',
                            json = data_load,
                            headers = headers)
        return (r.json())

#######DELETE TASK (ID)
@app.route('/user/task/del/<nb>', methods=['GET', 'POST'])
def route_delete_task(nb):
    if app.id == -1:
        return jsonify(api_delete_task(nb, app.id, 0))
    return jsonify(api_delete_task(nb, app.id, delete_task(int(nb))))

#######SEE ALL USERS
@app.route('/allusers', methods=['GET'])
def route_all_users():
    result = ""
    try:
        connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                              user=DATABASE_USER, passwd=DATABASE_PASS,
                              db=DATABASE_NAME)
        cursor = connect.cursor()
        cursor.execute("SELECT * from user")
        result = cursor.fetchall()
        cursor.close()
        connect.close()
    except Exception as e:
        print(f"Caught an exception : {e}")
    return jsonify(result)
