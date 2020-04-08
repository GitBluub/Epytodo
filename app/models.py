import pymysql as sql
from flask import g


def create_user(user_id, username, password):
    g.cursor.execute("INSERT INTO user (user_id, username, password)" +
                     f"VALUES('{user_id}', '{username}', '{password}');")
    g.sql_db.commit()


def get_task_id_list():
    g.cursor.execute("SELECT task_id from task")
    result = g.cursor.fetchall()
    list_task_id = [int(i[0]) for i in result]
    return list_task_id


def get_user_id_list():
    g.cursor.execute("SELECT user_id from user")
    result = g.cursor.fetchall()
    list_user_id = [int(i[0]) for i in result]
    return list_user_id


def get_username_list():
    g.cursor.execute("SELECT username from user")
    result = g.cursor.fetchall()
    list_username = [i[0] for i in result]
    return list_username


def get_password_list():
    g.cursor.execute("SELECT password from user")
    result = g.cursor.fetchall()
    list_password = [i[0] for i in result]
    return list_password


def get_task_list():
    g.cursor.execute("SELECT * from task")
    result = g.cursor.fetchall()
    task_list = [i for i in result]
    return task_list


def get_task_name_list():
    g.cursor.execute("SELECT title from task")
    result = g.cursor.fetchall()
    list_task_name = [i[0] for i in result]
    return list_task_name


def get_user_has_task_table():
    g.cursor.execute("SELECT * from user_has_task")
    result = g.cursor.fetchall()
    return result


def find_uid_with_username(username):
    g.cursor.execute("SELECT username from user")
    result = g.cursor.fetchall()
    list_user = [i[0] for i in result]
    g.cursor.execute("SELECT user_id from user")
    result = g.cursor.fetchall()
    list_id = [i[0] for i in result]
    uid = list_id[list_user.index(username)]
    return uid


def get_task_list_no_uid():
    g.cursor.execute("SELECT * from task")
    result = g.cursor.fetchall()
    task_list = [i for i in result]
    return task_list


def task_create(task_id, title, begin, end, status, uid):
    g.cursor.execute(
                "INSERT INTO task (task_id, title, begin, end, status) VALUE" +
                f"S('{task_id}', '{title}', '{begin}', '{end}', '{status}');")
    g.cursor.execute(
                f"INSERT INTO user_has_task (fk_user_id, fk_task_id) " +
                f"VALUES('{uid}', '{task_id}');")
    g.sql_db.commit()


def delete_task(task_id):
    g.cursor.execute(f"DELETE FROM task WHERE task_id = '{task_id}';")
    g.sql_db.commit()


def update_task(task_id, title, begin, end, status):
    delete_task(task_id)
    task_create(task_id, title, begin, end, status)
    g.sql_db.commit()


def create_new_user(username, password):
    if username is None or password is None:
        return -1
    g.cursor.execute("SELECT username from user")
    result = g.cursor.fetchall()
    list_username = [i[0] for i in result]
    if username in list_username:
        return 0
    g.cursor.execute("SELECT user_id from user")
    result = g.cursor.fetchall()
    list_user_id = [int(i[0]) for i in result]
    if (len(list_user_id) != 0):
        index_username = max(list_user_id) + 1
    else:
        index_username = 1
    g.cursor.execute(
                    f"INSERT INTO user (user_id, username, password)" +
                    f"VALUES('{index_username}', '{username}', '{password}');")
    g.sql_db.commit()
    return 1
