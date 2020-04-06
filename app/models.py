import pymysql as sql
from config import *
from random import *
import math
from app import app

def get_task_list_no_uid():
    connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                          user=DATABASE_USER, passwd=DATABASE_PASS,
                          db=DATABASE_NAME)
    cursor = connect.cursor()
    cursor.execute("SELECT * from task")
    result = cursor.fetchall()
    task_list = [i for i in result]
    cursor.close()
    connect.close()
    return task_list

def task_create(task_id, title, begin, end, status):
    connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                          user=DATABASE_USER, passwd=DATABASE_PASS,
                          db=DATABASE_NAME)
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO task (task_id, title, begin, end, status) VALUES('{task_id}', '{title}', '{begin}', '{end}', '{status}');")
    cursor.execute(f"INSERT INTO user_has_task (fk_user_id, fk_task_id) VALUES('{app.id}', '{task_id}');")
    connect.commit()
    cursor.close()
    connect.close()


def update_task(task_id, title, begin, end, status):
    connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                          user=DATABASE_USER, passwd=DATABASE_PASS,
                          db=DATABASE_NAME)
    cursor = connect.cursor()
    delete_task(task_id)
    task_create(task_id, title, begin, end, status)
    connect.commit()
    cursor.close()
    connect.close()

def get_date(string):
    print(string)
    month = {}
    month['Jan'] = '01'
    month['Feb'] = '02'
    month['Mar'] = '03'
    month['Apr'] = '04'
    month['May'] = '05'
    month['Jun'] = '06'
    month['Jul'] = '07'
    month['Aug'] = '08'
    month['Sep'] = '09'
    month['Oct'] = '10'
    month['Nov'] = '11'
    month['Dev'] = '12'
    array = string.split(' ')
    result = str(array[3]) + '-'
    result = result + month(array[2]) + '-'
    result = result + str(array[1]) + ' '
    result = result + str(array[4])


def delete_task(task_id):
    connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                          user=DATABASE_USER, passwd=DATABASE_PASS,
                          db=DATABASE_NAME)
    cursor = connect.cursor()
    cursor.execute("SELECT task_id from task")
    result = cursor.fetchall()
    list_task_id = [int(i[0]) for i in result]
    if int(task_id) not in list_task_id:
        return 0
    cursor.execute(f"DELETE FROM task WHERE task_id = '{task_id}';")
    connect.commit()
    cursor.close()
    connect.close()
    return 1


def create_new_task(name, debut, end, status):
    connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                          user=DATABASE_USER, passwd=DATABASE_PASS,
                          db=DATABASE_NAME)
    cursor = connect.cursor()
    cursor.execute("SELECT user_id from user")
    result = cursor.fetchall()
    list_user_id = [i[0] for i in result]
    if app.id not in list_user_id:
        return 0
    cursor.execute("SELECT title from task")
    result = cursor.fetchall()
    list_task_name = [i[0] for i in result]
    if name in list_task_name:
        return 0
    cursor.execute("SELECT task_id from task")
    result = cursor.fetchall()
    list_task_id = [int(i[0]) for i in result]
    if (len(list_task_id) != 0):
        task_id = max(list_task_id) + 1
    else:
        task_id = 1
    if status not in ('not started', 'in progress', 'done'):
        status = 'not started'
    cursor.execute(f"INSERT INTO task (task_id, title, begin, end, status) VALUES('{task_id}', '{name}', '{debut}', '{end}', '{status}');")
    cursor.execute(f"INSERT INTO user_has_task (fk_user_id, fk_task_id) VALUES('{app.id}', '{task_id}');")
    connect.commit()
    cursor.close()
    connect.close()
    return 1


def create_new_user(username, password):
    connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                          user=DATABASE_USER, passwd=DATABASE_PASS,
                          db=DATABASE_NAME)
    cursor = connect.cursor()
    cursor.execute("SELECT username from user")
    result = cursor.fetchall()
    list_username = [i[0] for i in result]
    if username in list_username:
        return 0
    cursor.execute("SELECT user_id from user")
    result = cursor.fetchall()
    list_user_id = [int(i[0]) for i in result]
    if (len(list_user_id) != 0):
        index_username = max(list_user_id) + 1
    else:
        index_username = 1
    cursor.execute(f"INSERT INTO user (user_id, username, password) VALUES('{index_username}', '{username}', '{password}');")
    connect.commit()
    cursor.close()
    connect.close()
    return 1


def sign_in_user(username, password):
    connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                          user=DATABASE_USER, passwd=DATABASE_PASS,
                          db=DATABASE_NAME)
    cursor = connect.cursor()
    cursor.execute("SELECT username from user")
    result = cursor.fetchall()
    list_user = [i[0] for i in result]
    cursor.execute("SELECT password from user")
    result = cursor.fetchall()
    list_password = [i[0] for i in result]
    cursor.execute("SELECT user_id from user")
    result = cursor.fetchall()
    list_id = [i[0] for i in result]
    cursor.close()
    connect.close()
    if username not in list_user:
        return 0
    if password not in list_password:
        return 0
    if password == list_password[list_user.index(username)]:
        app.id = list_id[list_user.index(username)]
        return 1
    return 0


def get_user_info(user_id):
    connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                          user=DATABASE_USER, passwd=DATABASE_PASS,
                          db=DATABASE_NAME)
    cursor = connect.cursor()
    cursor.execute("SELECT username from user")
    result = cursor.fetchall()
    list_user = [i[0] for i in result]
    cursor.execute("SELECT password from user")
    result = cursor.fetchall()
    list_password = [i[0] for i in result]
    cursor.execute("SELECT user_id from user")
    result = cursor.fetchall()
    list_id = [i[0] for i in result]
    result = {}
    infos = {}
    cursor.close()
    connect.close()
    for i in range(len(list_id)):
        if user_id == list_id[i]:
            infos["key1"] = list_user[i]
            infos["key2"] = list_password[i]
            result['result'] = infos
            return (result)
    result['error'] = "you must be logged in"
    return result


def get_task_info(user_id, task_id):
    connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                          user=DATABASE_USER, passwd=DATABASE_PASS,
                          db=DATABASE_NAME)
    if (user_id == -1):
        result = {}
        result['error'] = "you must be logged in"
        return result
    cursor = connect.cursor()
    cursor.execute("SELECT * from task")
    result = cursor.fetchall()
    task_list = [i for i in result]
    cursor.close()
    connect.close()
    for i in task_list:
        if (int(i[0]) == int(task_id)):
            result = {}
            info = {}
            info["title"] = i[1]
            info["begin"] = str(i[2])
            info["end"] = str(i[3])
            info["status"] = i[4]
            result['result'] = info
            return (result)
    result = {}
    result['error'] = "task id does not exist"
    return (result)


def get_task_list(user_id):
    connect = sql.connect(host=DATABASE_HOST, unix_socket=DATABASE_SOCK,
                          user=DATABASE_USER, passwd=DATABASE_PASS,
                          db=DATABASE_NAME)
    task_list = []
    if (user_id == -1):
        result = {}
        result['error'] = "you must be logged in"
        return result
    cursor = connect.cursor()
    cursor.execute("SELECT * from user_has_task")
    result = cursor.fetchall()
    for i in result:
        if int(i[0]) == user_id:
            task_list += [int(i[1])]
    cursor.execute("SELECT * from task")
    result = cursor.fetchall()
    full_list = {}
    task = []
    for i in result:
        if int(i[0]) in task_list:
            info = {}
            tmp = {}
            info["title"] = i[1]
            info["begin"] = str(i[2])
            info["end"] = str(i[3])
            info["status"] = i[4]
            tmp[str(i[0])] = info
            task += [tmp]
    final = {}
    dictionary = {}
    dictionary['task'] = task
    final['result'] = dictionary
    return (final)
