import pymysql as sql
from flask import Flask, g

import config as cf
from app import views
from app.views import blueprint


def app_factory():
    app = Flask(__name__, static_folder="app/static")
    app.config.from_object('config')
    app.secret_key = "dqzldqz$dlqz"
    return app


def get_db():
    if 'sql_db' not in g:
        g.sql_db = sql.connect(host=cf.DATABASE_HOST,
                               unix_socket=cf.DATABASE_SOCK,
                               user=cf.DATABASE_USER, passwd=cf.DATABASE_PASS,
                               db=cf.DATABASE_NAME)
        g.cursor = g.sql_db.cursor()


def teardown_db(error):
    if hasattr(g, "sql_db"):
        g.sql_db.close()
        g.cursor.close()
        g.pop("sql_db", None)
        g.pop("cursor", None)


def main():
    epytodo = app_factory()
    with epytodo.app_context():
        get_db()
    epytodo.before_request(get_db)
    epytodo.teardown_appcontext(teardown_db)
    epytodo.register_blueprint(blueprint, url_prefix="/")
    epytodo.run(debug=True)


if __name__ == "__main__":
    main()
