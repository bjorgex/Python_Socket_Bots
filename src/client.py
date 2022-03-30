#!/usr/bin/env python
from socket import *
import bots
from helpmethods import *

"""
The client will do the following:
1. Create a TCP socket and connect to (ip, port)
"""
HOST = 'localhost'
PORT = 5000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024
c = socket(AF_INET, SOCK_STREAM)  # TCP socket for IPv4
c.connect(ADDRESS)  # Connects to host server and added in a list of connected clients

welc_mesg = getSocketMsg(c, BUFSIZE)  # Get welcome msg
print(welc_mesg)
run_loop = True
no_name = True
failed_attempts = 0
_bots = ["alice", "bob", "dora", "chuck"]
name = ""
while True:
    while run_loop:
        name = input("This clients name is: ")  # Pick which bot you want to use by name
        for bot in _bots:
            if bot == name:
                run_loop = False
                no_name = False
                break
        failed_attempts = failed_attempts + 1
        if failed_attempts > 3:
            break
    # End of loop

    if not no_name:
        sendSocketMsg(c, name)  # Sends name to host

        """
        2. Read from the socket, line by line.
        a. If the line is from the host, you can expect it to be a suggestion, e.g. "Let's
        take a walk" or "Why don't we sing?". Extract the suggested action from the
        line. E.g. "walk" or "sing".
        """
        while True:
            """Wait fro record list"""
            record = c.recv(BUFSIZE)  # Recives a record list, should say no messages yet when first recieved
            if not record:
                print("Server disconnected")
                break
            print("Print Record: ")
            print(record.decode('utf-8'))  # Prints record list

            _suggestion = getSocketMsg(c, BUFSIZE)  # Get suggestion
            if not _suggestion:
                print("Server disconnected")
                break

            print("Print suggestion: ")
            print(_suggestion)
            _action1 = getSocketMsg(c, BUFSIZE)
            print("Action1 got: {}".format(_action1))
            _action2 = getSocketMsg(c, BUFSIZE)
            print("Action2 got: {}".format(_action2))

            """
            i. Call the function bot to create a response. Send the response back
            over the socket.
            """
            _response = callBot(name, _action1, _action2)  # Call bot, the bot will
            print("Print response: ")
            print(_response)
            sendSocketMsg(c, _response)    # Sends responds to host
            """
            ii. You can choose to remember the suggested action as alternative 1.
            """
            # _alt1 = _action
        """
        b. If the line is from one of the other participants, you can choose to ignore it,
        or pass it to your bot as alternative 2 if there's already a suggested action.

        3. You are free to decide how and when to end the connection.
        4. sending a message that might be dropped if the client is not ready to receive
        messages (optional)
        """
        c.close()
    else:
        print("To many failed attempts, closing client connection to server")
        c.close()
        break
