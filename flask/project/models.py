# models.py

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, name, password):
        self.id = name
        self.password = password

class Target():
    def __init__(self, uuid, name, hosts, owner):
        self.uuid = uuid
        self.name = name
        self.hosts = hosts
        self.owner = owner
