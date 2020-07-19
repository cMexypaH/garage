class Users:
    def __init__(self, mac):
        self.mac = mac
        self.name = mac
        self.role = ''

    def set_name(self, name):
        self.name = name

    def set_role(self, role):
        self.role = role

    def get_name(self):
        return self.name

    def get_role(self):
        return self.role

    def get_mac(self):
        return self.mac
