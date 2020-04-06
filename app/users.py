from flask_login import UserMixin
from .__init__ import login_manager


class User(UserMixin):
    id = -1
    authenticated = 0
    username = ""
    password = ""

    def is_authenticated(self):
        if (self.authenticated):
            return True
        return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        if self.authenticated:
            return str(self.id)
        return None
