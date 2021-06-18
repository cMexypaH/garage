import os
from threading import Thread

import RPi.GPIO as GPIO
import time
import logger
import fileHandler
from classes import Users

logger.init()

global user_good

ROLE_ENTRANCE = 1
ROLE_GARAGE = 2
ROLE_RAW = 3
ROLE_ADMIN = 4
ROLE_OWNER = 5

USERS_FILE = "/home/pi/garage/users.txt"

RAW_COMMAND = 'raw'     # raw:11:h:3
SIMPLE_COMMAND = 'c'    # c:openentrance:5
USER_NAME = 'u'         # u:username

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
pin_list = [11, 13, 15, 16]
GPIO.setup(pin_list, GPIO.OUT)


def command(recieved_data, user):
    rtrn = ""
    try:
        if recieved_data.startswith("[users]") and int(user.role) >= ROLE_ADMIN:
            users = recieved_data.replace("[users]", '')
            users = users.replace("\\n", '\n')
            fileHandler.writeall(USERS_FILE, users)
        else:
            parsed_data = recieved_data.split(':')
            type_command = parsed_data[0]
            if user.name != user.mac:  # ako usera sushtestvuva
                u_role = int(user.role)
                global user_good
                if type_command == USER_NAME and user.name != parsed_data[1]:
                    rtrn = "ERROR:Cannot change username"
                    user_good = False
                elif type_command == USER_NAME and user.name == parsed_data[1]:
                    rtrn = "Welcome " + user.name
                    user_good = True
                elif type_command == RAW_COMMAND and u_role >= ROLE_RAW and user_good is True:
                    parsed_command = parsed_data[1].split(';')
                    pin_number = int(parsed_command[0])
                    is_high = True
                    if parsed_command[1] == 'l':
                        is_high = False
                    if len(parsed_command) == 3:
                        delay = int(parsed_command[2])
                        Thread(target=controlPins, args=(pin_number, delay,)).start()
                        rtrn += f"Pin {pin_number} is {is_high} for {delay} seconds"
                    elif len(parsed_command) == 2:
                        GPIO.output(pin_number, is_high)
                        rtrn += f"Pin {pin_number} is {is_high} "
                elif type_command == SIMPLE_COMMAND and user_good is True:
                    command = parsed_data[1]
                    if command == "opengarage" and u_role >= ROLE_GARAGE:
                        Thread(target=controlPins, args=(11, 0.1,)).start()
                        rtrn += "Garage is opening"
                    if command == "closegarage" and u_role >= ROLE_GARAGE:
                        Thread(target=controlPins, args=(13, 0.1,)).start()
                        rtrn += "Garage is closing"
                    if command == "stopgarage" and u_role >= ROLE_GARAGE:
                        Thread(target=controlPins, args=(15, 0.1,)).start()
                        rtrn += "Garage is stopped"
                    if command == "openentrance" and u_role >= ROLE_ENTRANCE:
                        timeentrance = int(parsed_data[2])
                        Thread(target=controlPins, args=(16, timeentrance,)).start()
                        rtrn += f"Entrance unlocked for {timeentrance} seconds"
                    if parsed_data[1] == 'restart' and u_role >= ROLE_ADMIN:
                        rtrn += "Restarting"
                        os.system('reboot')
                    if command == "getusers" and u_role >= ROLE_ADMIN:
                        userlist = str(fileHandler.read(USERS_FILE))[1:-1]
                        userlist = userlist.replace("'", "")
                        userlist = userlist.replace(",", "")
                        userlist = userlist.replace(" ", "")
                        rtrn = "[users]" + userlist
                else:
                    rtrn += "Wrong command!"
            else:
                if type_command == USER_NAME:
                    rec_username = parsed_data[1]
                    fileHandler.write(USERS_FILE, rec_username, user.mac, "0")
                    user.name = rec_username
                    user.role = 0
                    rtrn += "User created"
    except (ValueError, IndexError, Exception) as e:
        print(e)
        return str.encode("!!! ERROR - check logs !!!")
    return rtrn


def controlPins(pinNumber, waitTime):
    GPIO.output(pinNumber, True)
    time.sleep(waitTime)
    GPIO.output(pinNumber, False)


def checkUserMac(mac):
    users = fileHandler.read(USERS_FILE)
    us = Users(mac)
    if users is not None:
        for user in users:
            if user != '\n':
                u = user.split(';')
                if u[1] == mac:
                    us.name = u[0]
                    us.role = u[2]
                    return us
    return us
