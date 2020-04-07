import pymysql as sql

from app import app

from .post_request import get_uid
from .models import (create_user, get_password_list, get_task_id_list,
                     get_task_list, get_task_list_no_uid, get_task_name_list,
                     get_user_has_task_table, get_user_id_list,
                     get_username_list, task_create, update_task)


def create_new_user(username, password):
    if username is None or password is None:
        return -1
    list_username = get_username_list()
    if username in list_username:
        return 0
    list_user_id = get_user_id_list()
    if list_user_id:
        user_id = max(list_user_id) + 1
    else:
        user_id = 1
    create_user(user_id, username, password)
    return 1


def sign_in_user(username, password):
    list_user = get_username_list()
    list_password = get_password_list()
    list_id = get_user_id_list()
    if username not in list_user:
        return -1
    if password == list_password[list_user.index(username)]:
        return list_id[list_user.index(username)]
    return 0


def get_user_info(user_id):
    if user_id == -1:
        return {"error": "you must be logged in"}
    list_user = get_username_list()
    list_password = get_password_list()
    list_id = get_user_id_list()
    for i in range(len(list_id)):
        if user_id == list_id[i]:
            infos = {"key1": list_user[i],
                     "key2": list_password[i]}
            return {"result": infos}
    return {"error": "internal error"}


def get_task_info(user_id, task_id):
    if (user_id == -1):
        return {"error": "you must be logged in"}
    task_list = get_task_list()
    for i in task_list:
        if (int(i[0]) == int(task_id)):
            info = {"title": i[1],
                    "begin": str(i[2]),
                    "end": str(i[3]),
                    "status": i[4]}
            return {"result": info}
    return {"error": "task id does not exist"}


def get_task_list_of_uid(user_id):
    if (user_id == -1):
        return {"error": "you must be logged in"}
    usr_has_task = get_user_has_task_table()
    task_list_user = [int(i[1]) for i in user_has_task if int(i[0]) == user_id]
    task_list = get_task_list()
    task = []
    for i in task_list:
        if int(i[0]) in task_list_user:
            info = {"title": i[1],
                    "begin": str(i[2]),
                    "end": str(i[3]),
                    "status": i[4]}
            task += [{str(i[0]): info}]
    dictionary = {'task': task}
    return {"result": dictionary}


def modify_task(task_id, data):
    title = data.get('title')
    begin = data.get('begin')
    end = data.get('end')
    status = data.get('status')
    if status is None or title is None or begin is None or end is None:
        return ({"error": "internal error"})
    if not status or not begin or not end or not title:
        return ({"error": "internal error"})
    if status not in ["in progress", "done", "not started"]:
        status = "not started"
    task_list = get_task_list_no_uid()
    task_id_list = [int(i[0]) for i in task_list]
    if int(task_id) not in task_id_list:
        return ({"error": "task id does not exist"})
    update_task(task_id, title, begin, end, status)
    return ({"result": "update done"})


def create_new_task(name, begin, end, status):
    list_user_id = get_user_id_list()
    if get_uid() not in list_user_id:
        return 0
    list_task_name = get_task_name_list()
    if name in list_task_name:
        return 0
    list_task_id = get_task_id_list()
    task_id = max(list_task_id) + 1 if list_task_id else 1
    if status not in ('not started', 'in progress', 'done'):
        status = 'not started'
    task_create(task_id, name, begin, end, status)
    return 1


def delete_selected_task(task_id):
    list_task_id = get_task_id_list()
    if int(task_id) not in list_task_id:
        return 0
    delete_task(task_id)
    return 1


def get_all_users():
    result = ""
    try:
        app.cursor.execute("SELECT * from user")
        result = app.cursor.fetchall()
    except Exception as e:
        print(f"Caught an exception : {e}")
    return (result)
