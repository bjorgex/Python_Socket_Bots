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
-A good program will check if clients are still connected before trying to interact with them. If they're not, or if you decide that they're
taking too long to respond, you can remove them from the list of connections.
5. You are free to decide when and how to disconnect the clients (you can
even kick them out if they misbehave) and how to gracefully terminate the program.
6. Make a "bot" that takes its response from the command line. That way you
or other users can interact with the bots and make the dialogue more interesting.
7. Don't nag your users. It's sometimes nice to let the user add choices and
options, but your defaults should work well without user interaction. Don't make them fill out
forms
"""
import time
from socket import *
from threading import Thread
from time import ctime
from chatrecord import ChatRecord
from bots import __action__
from helpmethods import *


class ClientHandler(Thread):
    """Handles a client request."""

    def __init__(self, client, record):
        Thread.__init__(self)
        self._name = None
        self._client = client
        self._record = record

    def run(self):
        msg = "Welcome to the chat room!"                       # welcome msg
        sendSocketMsg(self._client, msg)                        # Sends welcome msg
        self._name = getSocketMsg(self._client, BUFSIZE)        # Gets client name and decodes it
        print("Client name received: {}".format(self._name))    # Prints to client name to console
        clientNamesRecieved.append(self._name)                  # When enough clients names have been added, this will break the loop in server.py
        record_msg = str(self._record).encode('utf-8')          # Encodes the record list
        self._client.send(record_msg)                           # Sends the record list to client
        print("Server sent record list to client")
        #########################################
        while True:
            """Waits for response from client"""
            _response = getSocketMsg(self._client, BUFSIZE)               # Receives message from bot
            print("Dont og past")
            if not _response:
                print("Client disconnected")
                connected_clients.remove(self._client)
                self._client.close()
                break
            else:
                _response = self._name + ' ' + ctime() + '\n' + _response
                self._record.add(_response)
                self._client.send(str(self._record).encode('utf-8'))


HOST = 'localhost'
PORT = 5000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024

record = ChatRecord()
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDRESS)
cRoof = 1
server.listen(2)

connected_clients = []  # List of all connected clients
clientNamesRecieved = []
_round = 0
"""
The server now waits for connections from clients,
and hands sockets off to clients handlers
"""
while True:
    # Gather cRoof clients
    print('Waiting for connections...')
    print("There are " + str(len(connected_clients)) + " connected clients")
    client, address = server.accept()
    print('... connected from: ', address)
    handler = ClientHandler(client, record)
    handler.start()
    # Appends client name to connected clients
    connected_clients.append(client)
    if len(connected_clients) == cRoof:
        print("cRoof reached \n")
        while True:
            """Wait for all clients to have sent their name"""
            while len(clientNamesRecieved) != cRoof:
                """Loops around until clients are recieved"""
                print("Need to receive ", cRoof - len(clientNamesRecieved), " more bot names")
                time.sleep(5)

            print("All names recieved")
            print("Sending suggestion")
            # Picks either one or two actions, if only one is choosen, _action2 will = null
            _action1, _action2 = __action__()
            print(_action1, " And ",_action2)
            # Create suggestion with the actions
            if not _action2:
                msg = "Would any of you want to {}?".format(_action1)
            else:
                msg = "Would any of you want to {}? Or maybe {}?".format(_action1, _action2)

            record.add(msg)     # Add suggestion to record

            for client in connected_clients:
                sendSocketMsg(client, msg)  # Sends msg from host to clients
                sendSocketMsg(client, _action1)
                sendSocketMsg(client, _action2)

            _round = _round + 1
            print("Round ", _round, " starts now!")

            time.sleep(10)


