import pymysql as sql
from config import *
from app import app
from .models import get_task_list_no_uid, update_task

def modify_task(task_id, data):
    title = data.get('title')
    begin = data.get('begin')
    end = data.get('end')
    status = data.get('status')
    if status == None or title == None or begin == None or end == None:
        return ({"error":"internal error"})
    if not len(status) or not len(begin) or not len(end) or not len(title):
        return ({"error":"internal error"})
    if status not in ["in progress", "done", "not started"]:
        status = "not started"
    task_list = get_task_list_no_uid()
    task_id_list = [int(i[0]) for i in task_list]
    if int(task_id) not in task_id_list:
        return ({"error":"task id does not exist"})
    update_task(task_id, title, begin, end, status)
    return ({"result":"update done"})

def get_all_users():
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
    return (result)
