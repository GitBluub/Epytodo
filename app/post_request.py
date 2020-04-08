import requests
from flask import session

from config import HOST_URL


def get_uid():
    return int(session.get("user_id", -1))


def make_post_register(username, password, uid):
    cookie_jar = {}
    if uid is not None:
        cookie_jar = {"user_id": str(uid)}
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}
    data_load = {"username": username,
                 "password": password}
    resp = requests.post(HOST_URL + 'register',
                         json=data_load,
                         headers=headers,
                         cookies=cookie_jar)
    return resp.json()


def make_post_signin(username, password, uid):
    cookie_jar = {}
    if uid is not None:
        cookie_jar = {"user_id": str(uid)}
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}
    data_load = {"username": username,
                 "password": password}
    resp = requests.post(HOST_URL + 'signin',
                         json=data_load,
                         headers=headers,
                         cookies=cookie_jar)
    return resp.json()


def make_post_change(data_load, uid):
    cookie_jar = {}
    if uid is not None:
        cookie_jar = {"user_id": str(uid)}
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}
    resp = requests.post(HOST_URL + f'user/task/{nb}',
                         json=data_load,
                         headers=headers,
                         cookies=cookie_jar)
    return resp.json()


def make_post_create(name, begin, end, status, uid):
    cookie_jar = {}
    if uid is not None:
        cookie_jar = {"user_id": str(uid)}
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}
    data_load = {"title": name,
                 "begin": begin,
                 "end": end,
                 "status": status}
    resp = requests.post(HOST_URL + 'user/task/add',
                         json=data_load,
                         headers=headers,
                         cookies=cookie_jar)
    return resp.json()
