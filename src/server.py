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
        msg = "Welcome to the chat room!".encode('utf-8')       # Encodes the welcome msg
        self._client.send(msg)                                  # Sends welcome msg
        print("Welcome message sent")                           # Prints to console
        name = self._client.recv(BUFSIZE)                       # Receive name of the client chosen bot
        self._name = name.decode('utf-8')                       # Client name decoded
        print("Client name received: {}".format(self._name))    # Prints to client name to console
        record_msg = str(self._record).encode('utf-8')          # Encodes the record list
        self._client.send(record_msg)                           # Sends the record list to client
        print("Server sent record list to client")
        #########################################
        while True:
            message = self._client.recv(BUFSIZE)                # Recives message from bot
            print("Recieved message from client")
            if not message:
                print("Client disconnected")
                connected_clients.remove(client)
                self._client.close()
                break
            else:
                message = self._name.decode('utf-8') + ' ' + ctime() + '\n' + message.decode('utf-8')
                self._record.add(message)
                self._client.send(str(self._record).encode('utf-8'))


HOST = 'localhost'
PORT = 5000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024

record = ChatRecord()
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDRESS)
cRoof = 1
server.listen(cRoof)
"""List of all connected clients"""
connected_clients = []
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
    connected_clients.append(client)               # Appends client name to connected clients
    if connected_clients == cRoof:
        print("if state")
        # Pick your own action or a random one
        _action = __action__()
        # Add the initial statement to record
        message = "Would any of you want to {}?".format(_action)
        record.add(message)
        # Send statement to clients
        server.send(_action.encode('utf-8'))
