

def read(fName):
    with open(fName, 'r') as reader:
        ls = list(reader)
    return ls

def write(fName, username, mac, role):
    with open(fName, 'a') as a_writer:
        a_writer.write(username + ';' + mac + ';' + role + '\n')
