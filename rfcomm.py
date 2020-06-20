import os
import glob
import time
import threading
import bluetooth
from bluetooth import *
import commands
import logging

global server_sock, port

def init_server():
    global server_sock, port
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


def listen_for_connection():
    global server_sock, port, client_sock, client_info
    print("Waiting for connection on RFCOMM channel %d" % port)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)
    #new_thread()


def disconnecting():
    print(client_info, " disconnected")
    listen_for_connection()


def disconnect(c_sock, s_sock):
    print("disconnected")
    c_sock.close()
    s_sock.close()
    print("all done")


def recieving_data():
    while True:

        try:
            data = client_sock.recv(1024)
            data = data.decode('utf_8')
            data = data.lower()
            if len(data) == 0:
                disconnecting()
            print(f"<<< {data}")

            dt = commands.command(data)

            client_sock.send(dt)
            print(f">>> {dt}")

        except bluetooth.btcommon.BluetoothError:
            disconnecting()
            disconnect(client_sock, server_sock)
            pass
        except IOError:
            pass

        except KeyboardInterrupt:
            disconnect(client_sock, server_sock)
            break


def thread_function(name):
    logging.info("Thread %s: starting", name)
    init_server()
    listen_for_connection()
    logging.info("Thread %s: finishing", name)


def new_thread():
    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")

init_server()
listen_for_connection()
recieving_data()

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


