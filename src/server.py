#!/usr/bin/env python

"""
1. Accept any connection. You can expect all connections to be a bot, e.g. that
they will not be the first to speak, but that they will always respond. This gives you the option
of waiting for them. You can also decide to make your program more robust by reading from
clients in parallel, or if you're a real pro, use select or poll to make the clients non-blocking.
But keep in mind: it's better to have something simple that works than something
sophisticated that doesn't.
2. Initiate a round of dialogue by suggesting an action. Send the suggestion to
each of your connected clients. The action can be random, provided as user input for each.
3. All responses should be sent back out to all clients except the one who sent it.
4. Maintain a list of connected clients.
-If you want, you can let new connections wait until you've completed one round of dialogue.
-A good program will check if clients are still connected before trying to interact with them.
If they're not, or if you decide that they're
taking too long to respond, you can remove them from the list of connections.
5. You are free to decide when and how to disconnect the clients (you can
even kick them out if they misbehave) and how to gracefully terminate the program.
6. Make a "bot" that takes its response from the command line. That way you
or other users can interact with the bots and make the dialogue more interesting.
7. Don't nag your users. It's sometimes nice to let the user add choices and
options, but your defaults should work well without user interaction. Don't make them fill out
forms
"""
from socket import *
from threading import Thread
from time import ctime
from chatrecord import ChatRecord
from bots import __action__
from helpmethods import *
import random
import signal
import time
import sys

"""Traps"""


# Handles ctrl + c interrupts

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)


signal.signal(signal.SIGINT, handler)

"""ClientHandler class"""


# Start threads for clients

class ClientHandler(Thread):
    """Handles a client request."""

    def __init__(self, client, record):
        Thread.__init__(self)
        self._name = None
        self._client = client
        self._record = record

    def run(self):
        msg = "Welcome to the chat room!"  # welcome msg
        sendSocketMsg(self._client, msg)  # Sends welcome msg

        self._name = getSocketMsg(self._client, BUFSIZE)  # Gets client name and decodes it
        if not self._name:
            print("Client disconnected fomr handler")
            print("Remove client from connected clients")
            connected_clients.remove(self._client)
            self._client.close()
            exit()

        print("Client name received: {}".format(self._name))  # Prints to client name to console
        clientNamesReceived.append(
            self._name)  # When enough clients names have been added, this will break the loop in server.py
        record_msg = str(self._record).encode('utf-8')  # Encodes the record list
        self._client.send(record_msg)  # Sends the record list to client
        print("Server sent record list to client")
        #########################################
        while True:
            """Waits for response from client"""
            _response = getSocketMsg(self._client, BUFSIZE)  # Receives message from bot
            print("Response from {}: {}".format(self._name, _response))
            if not _response:
                print("Client disconnected")
                connected_clients.remove(self._client)
                self._client.close()
                break
            else:
                _response = self._name + ' ' + ctime() + ': \n' + _response
                self._record.add(_response)
                recordAll.add(_response)
                self._client.send(str(self._record).encode('utf-8'))


HOST = 'localhost'
PORT = 5000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024
recordAll = ChatRecord()
record = ChatRecord()
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDRESS)
cRoof = 0
while True:
    cRoof = int(input("How many clients has to connect before the chat room host suggests something?: "))
    if isinstance(cRoof, int):
        break
    else:
        print("Error: Wrong input input. Only integers are accepted")

server.listen(cRoof)

connected_clients = []  # List of all connected clients
clientNamesReceived = []
_round = 0
"""
The server now waits for connections from clients,
and hands sockets off to clients handlers
"""
while True:
    # Gather cRoof clients
    print('Waiting for connections...')
    print("There is " + str(len(connected_clients)) + " connected clients")
    client, address = server.accept()
    print('... connected from: ', address)
    handler = ClientHandler(client, record)
    handler.start()
    time.sleep(2)
    # Appends client name to connected clients
    connected_clients.append(client)

    while len(connected_clients) == cRoof:
        print("Enough clients have joined the chat room \n")
        """Wait for all clients to have sent their name"""
        print("Retrieving bot names")
        while len(clientNamesReceived) != cRoof:
            """Loops around until client names are received"""
            print("Need to retrieve", cRoof - len(clientNamesReceived),
                  "more bot names")  # This should be removed or changed for finished code
            time.sleep(5)
            if not len(clientNamesReceived) < cRoof:
                break

        print("\nAll names received")
        print("Sending suggestion")
        # Picks either one or two actions, if only one is chosen, _action2 will = null
        _rand = random.choice([1, 2])

        if _rand == 1:
            _action1 = __action__(1)
            _action2 = "None"
            _suggestion = "Would any of you want to {}?".format(_action1)
            print("Action1: {}\nAction2: None".format(_action1))
        else:
            _action1, _action2 = __action__(2)
            _suggestion = "Would any of you want to {}? Or maybe {}?".format(_action1, _action2)
            print("Actions1: {}\nAction2: {}".format(_action1, _action2))

        _round = _round + 1
        print("Round ", _round, " starts now!\n-----------------------------------")
        print("Suggestion from host: {}".format(_suggestion))

        for client in connected_clients:
            sendSocketMsg(client, _suggestion)  # Sends _suggestion from host to clients
            sendSocketMsg(client, _action1)
            sendSocketMsg(client, _action2)

        time.sleep(5)
        print("\nHost record:.............\n{}\nEnd of Record....................".format(recordAll))

        while True:
            _choise = input("New round(R)? - Quit server(Q)\n"
                            "Write either R or Q here to choose: ")
            if _choise == "R":
                break
            elif _choise == "Q":
                for client in connected_clients:
                    sendSocketMsg(client, "Q")
                server.close()
                sys.exit("Quit chat bot")
            else:
                print("Error: Wrong input, try again!")
