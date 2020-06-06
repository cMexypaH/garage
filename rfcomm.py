import os
import glob
import time
import RPi.GPIO as GPIO
from bluetooth import *
import commands

connected = False

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))

server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "00001101-0000-1000-8000-00805f9b34fb"

advertise_service(server_sock, "GragePiServer",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  )


def is_connected():
    global connected
    try:
        client_sock.getpeername()
        connected = True
    except:
        connected = False


def listen_for_connection():
    global server_sock, port, client_sock, client_info
    print("Waiting for connection on RFCOMM channel %d" % port)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)


def disconnect(c_sock, s_sock):
    print("disconnected")
    c_sock.close()
    s_sock.close()
    print("all done")


listen_for_connection()

while True:

    try:
        data = client_sock.recv(1024)
        data = data.decode('ascii')
        data = data.lower()
        if len(data) == 0:
            #disconnect(client_sock, server_sock)
            listen_for_connection()
        print("received [%s]" % data)

        commands.command(data)

        client_sock.send(data)
        print("sending [%s]" % data)

    except IOError:
        pass

    except KeyboardInterrupt:
        disconnect(client_sock, server_sock)
        break
