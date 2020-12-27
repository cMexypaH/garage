

def read(fName):
    with open(fName, 'r') as reader:
        ls = list(reader)
    return ls


def write(fName, username, mac, role):
    with open(fName, 'a') as a_writer:
        a_writer.write(f'\n{username}')
        a_writer.write(';')
        a_writer.write(mac)
        a_writer.write(';')
        a_writer.write(role)
#        a_writer.write(username + ';' + mac + ';' + role + '\n')


def writeall(fName, data):
    with open(fName, 'w') as a_writer:
        a_writer.write(data)