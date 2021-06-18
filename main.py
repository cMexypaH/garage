#!/usr/bin/python

import time
import RPi.GPIO as GPIO
from bluetooth import *
from threading import *
import subprocess
import configparser
import commands
import logger
from classes import Users

logger.init()

global user_good


# Function for handling connections. This will be used to create threads
def clientthread(conn, cl_info):
    # infinite loop so that function do not terminate and thread do not end.
    countfordc = 0
    macaddr = cl_info[0].lower()
    user = commands.checkUserMac(macaddr)
    print(f"{macaddr} is {user.name}")
    while True:
        try:
            user = commands.checkUserMac(macaddr)
            # Receiving from client
            data = conn.recv(1024)
            data = data.decode('utf_8')
            data = data.lower()
            data = data.strip()
            if data == '':
                countfordc += 1
            else:
                print(f"Received: {data} from {user.name}")
                dt = commands.command(data, user)
                print(dt)
                conn.send(dt)
            if countfordc > 10:
                break
        except IOError:
            break

    # came out of loop
    print(f"{user.name} lost connection: Disconnected")
    conn.close()


#
# MAIN
#
time.sleep(20)

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "00001101-0000-1000-8000-00805f9b34fb"

advertise_service(server_sock, "Garage-pi",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  #                   protocols = [ OBEX_UUID ]
                  )

print("Waiting for connection on RFCOMM channel %d" % port)

while True:
    client_sock, client_info = server_sock.accept()
    user = Users(client_info[0])
    print(f"Accepted Bluetooth connection from {user.mac}")

    Thread(target=clientthread, args=(client_sock, client_info,)).start()

print("disconnected")
server_sock.close()
print("all done")
