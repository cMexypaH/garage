import json
from json import JSONEncoder


class Users:
    def __init__(self, mac):
        self.mac = mac
        self.name = mac
        self.role = ''
        self.isGood = False

    def set_name(self, name):
        self.name = name

    def set_role(self, role):
        self.role = role

    def set_isGood(self, isgood):
        self.isGood = isgood

    def get_isGood(self):
        return self.isGood

    def get_name(self):
        return self.name

    def get_role(self):
        return self.role

    def get_mac(self):
        return self.mac


class UserJSONEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__

