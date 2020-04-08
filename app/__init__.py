from functools import wraps

import pymysql as sql
import requests
from flask import Flask, abort, current_app

import config as cf

# TODO: Remove me
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "dqzldqz$dlqz"
app.connect = sql.connect(host=cf.DATABASE_HOST,
                          unix_socket=cf.DATABASE_SOCK,
                          user=cf.DATABASE_USER, passwd=cf.DATABASE_PASS,
                          db=cf.DATABASE_NAME)
app.cursor = app.connect.cursor()


def app_factory():
    # TODO: Setup application and register blueprints below
    app = Flask(__name__)
    app.config.from_object('config')
    app.secret_key = "dqzldqz$dlqz"
    # TODO: Do not create circular dependency, extract sql connection/cursor
    #       to a globally-available singleton. (See `flask.g`)
    app.connect = sql.connect(host=cf.DATABASE_HOST,
                              unix_socket=cf.DATABASE_SOCK,
                              user=cf.DATABASE_USER, passwd=cf.DATABASE_PASS,
                              db=cf.DATABASE_NAME)
    app.cursor = app.connect.cursor()
    return app
