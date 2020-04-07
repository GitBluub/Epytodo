import pymysql as sql

from app import app

from .post_request import get_uid


def create_user(user_id, username, password):
    app.cursor.execute("INSERT INTO user (user_id, username, password)" +
                       f"VALUES('{user_id}', '{username}', '{password}');")
    app.connect.commit()


def get_task_id_list():
    app.cursor.execute("SELECT task_id from task")
    result = app.cursor.fetchall()
    list_task_id = [int(i[0]) for i in result]
    return list_task_id


def get_user_id_list():
    app.cursor.execute("SELECT user_id from user")
    result = app.cursor.fetchall()
    list_user_id = [int(i[0]) for i in result]
    return list_user_id


def get_username_list():
    app.cursor.execute("SELECT username from user")
    result = app.cursor.fetchall()
    list_username = [i[0] for i in result]
    return list_username


def get_password_list():
    app.cursor.execute("SELECT password from user")
    result = app.cursor.fetchall()
    list_password = [i[0] for i in result]
    return list_password


def get_task_list():
    app.cursor.execute("SELECT * from task")
    result = app.cursor.fetchall()
    task_list = [i for i in result]
    return task_list


def get_task_name_list():
    app.cursor.execute("SELECT title from task")
    result = app.cursor.fetchall()
    list_task_name = [i[0] for i in result]
    return list_task_name


def get_user_has_task_table():
    app.cursor.execute("SELECT * from user_has_task")
    result = app.cursor.fetchall()
    return result


def find_uid_with_username(username):
    app.cursor.execute("SELECT username from user")
    result = app.cursor.fetchall()
    list_user = [i[0] for i in result]
    app.cursor.execute("SELECT user_id from user")
    result = app.cursor.fetchall()
    list_id = [i[0] for i in result]
    uid = list_id[list_user.index(username)]
    return uid


def get_task_list_no_uid():
    app.cursor.execute("SELECT * from task")
    result = app.cursor.fetchall()
    task_list = [i for i in result]
    return task_list


def task_create(task_id, title, begin, end, status):
    app.cursor.execute(
                "INSERT INTO task (task_id, title, begin, end, status) VALUE" +
                f"S('{task_id}', '{title}', '{begin}', '{end}', '{status}');")
    app.cursor.execute(
                f"INSERT INTO user_has_task (fk_user_id, fk_task_id) " +
                f"VALUES('{get_uid()}', '{task_id}');")
    app.connect.commit()


def delete_task(task_id):
    app.cursor.execute(f"DELETE FROM task WHERE task_id = '{task_id}';")
    app.connect.commit()


def update_task(task_id, title, begin, end, status):
    delete_task(task_id)
    task_create(task_id, title, begin, end, status)
    app.connect.commit()


def create_new_user(username, password):
    if username is None or password is None:
        return -1
    app.cursor.execute("SELECT username from user")
    result = app.cursor.fetchall()
    list_username = [i[0] for i in result]
    if username in list_username:
        return 0
    app.cursor.execute("SELECT user_id from user")
    result = app.cursor.fetchall()
    list_user_id = [int(i[0]) for i in result]
    if (len(list_user_id) != 0):
        index_username = max(list_user_id) + 1
    else:
        index_username = 1
    app.cursor.execute(
                    f"INSERT INTO user (user_id, username, password)" +
                    f"VALUES('{index_username}', '{username}', '{password}');")
    app.connect.commit()
    return 1
