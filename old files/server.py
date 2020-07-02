# Importing the Bluetooth Socket library
import bluetooth

import commands

host = ""
port = 1  # Raspberry Pi uses port 1 for Bluetooth Communication
# Creaitng Socket Bluetooth RFCOMM communication
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print('Bluetooth Socket Created')
try:
    server.bind((host, port))
    print("Bluetooth Binding Completed")
except:
    print("Bluetooth Binding Failed")
server.listen(1)  # One connection at a time
# Server accepts the clients request and assigns a mac address.
client, address = server.accept()
print("Connected To", address)
print("Client:", client)
try:
    while True:
        # Receivng the data.
        data = client.recv(1024)  # 1024 is the buffer size.
        print(data)

        commands.command(data)
        # Sending the data.
        client.send("RECIEVED DATA: " + data)
except:
    # Closing the client and server connection
    client.close()
    server.close()