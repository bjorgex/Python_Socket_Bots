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

HOST = 'localhost'
PORT = 5000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024

c = socket(AF_INET, SOCK_STREAM)   # TCP socket for IPv4
c.connect(ADDRESS)
print(c.recv(BUFSIZE))
name = input("Enter your name")
c.send(name)

while True:
    record = c.recv(BUFSIZE)
    if not record:
        print("Server disconnected")
        break
    print(record)
    message = input("> ")
    if not message:
        print("Server disconnected")
        break
    c.send(message + "\n")
c.close()
