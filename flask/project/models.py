# models.py

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, name, password):
        self.id = name
        self.password = password
