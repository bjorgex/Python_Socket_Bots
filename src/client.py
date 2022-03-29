#!/usr/bin/env python

"""
The client will do the following:
1. Create a TCP socket and connect to (ip, port)
2. Read from the socket, line by line.
a. If the line is from the host, you can expect it to be a suggestion, e.g. "Let's
take a walk" or "Why don't we sing?". Extract the suggested action from the
line. E.g. "walk" or "sing".
i. Call the function bot to create a response. Send the response back
over the socket.
ii. You can choose to remember the suggested action as alternative 1.
b. If the line is from one of the other participants, you can choose to ignore it,
or pass it to your bot as alternative 2 if there's already a suggested action.
3. You are free to decide how and when to end the connection.
4. sending a message that might be dropped if the client is not ready to receive
messages (optional)
"""

from socket import *
import bots
from helpmethods import *

HOST = 'localhost'
PORT = 5000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024

c = socket(AF_INET, SOCK_STREAM)  # TCP socket for IPv4

"""Connects to host server and added in a list of connected clients"""
c.connect(ADDRESS)
# ClientHandler() function gets called
getSocketMsg(c, BUFSIZE)  # Get welcome msg
name = input(b'Enter your name: ')  # Pick which bot you want to use by name
sendSocketMsg(c, name)              # Sends name to host
print("Waiting for record list")

while True:
    record = c.recv(BUFSIZE)                    # Recieves record list from host
    print("Recieved record list from server")
    record = record.decode('utf-8')             # Decodes record list

    if not record:  # If there is no data in record list do this
        print('Server disconnected')
        break
    print(record)   # Prints record list

    _action = c.recv(BUFSIZE).decode('utf-8')   # Recieves and decodes action
    message = bots.alice(_action)

    if not message:
        print('Server disconnected')
        break
    send_msg = message + '\n'
    c.send(send_msg.encode('utf-8'))

c.close()
