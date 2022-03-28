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
import bots
from helpmethods import *


class ClientHandler(Thread):
    """Handles a client request."""

    def __init__(self, client, record):
        Thread.__init__(self)
        self._name = None
        self._client = client
        self._record = record

    def run(self):
        msg = "Welcome to the chat room! Sorry that you had to wait for the other clients".encode(
            'utf-8')  # Encodes the welcome msg
        self._client.send(msg)  # Sends welcome msg
        print("Welcome message sent")  # Prints to console
        name = self._client.recv(BUFSIZE)  # Receive name of the client chosen bot
        self._name = name.decode('utf-8')  # Client name decoded
        print("Client name received")  # Prints to console

        """
    
        record_msg = str(self._record).encode('utf-8')  # Encodes the record list
        self._client.send(record_msg)  # Sends the record list to client
        print("Server sent record list to client")
        self._client.send(action.encode('utf-8'))
        print("Sent action to client")
        while True:
            message = self._client.recv(BUFSIZE)
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
        """


HOST = 'localhost'
PORT = 5000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024

record = ChatRecord()
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDRESS)
server.listen(5)
"""List of all connected clients"""
connected_clients = []
"""
The server now waits for connections from clients,
and hands sockets off to clients handlers
"""
while True:
    print('Waiting for connections...')
    print("There are " + str(len(connected_clients)) + " connected clients")
    client, address = server.accept()
    connected_clients.append(client)
    print('... connected from: ', address)
    if len(connected_clients) == 5:
        _round = 0
        while True:
            _round = _round + 1
            """
            For loop that starts a thread for the 5 different clients.
            Before ClientHandler is called on the client.
            valEstasblishedConnection() checks the connection beforehand.
            If it returns false, we remove the client from connected_clients and,
            listens continue the chat without the removed client
            """
            Nr = 1
            clientCount = len(connected_clients)
            for client in connected_clients:
                print(client)
                if valEstasblishedConnection(client, Nr):
                    handler = ClientHandler(client, record)
                    handler.start()
                    Nr = Nr + 1
                else:
                    print("Client{}: {} disconnected, removing from connected clients".format(Nr, client))
                    connected_clients.remove(client)

            newClientCount = len(connected_clients)
            clientsGone = clientCount - newClientCount
            print("There are now {} clients, {} have been disconnected".format(newClientCount, clientsGone))

            print("Round {} starts... ".format(_round))
            print("{} clients have now connected, host proceeds to ask the clients a question with an action".format(newClientCount))
            """The actions"""
            a = bots.__action__()
            """The question"""
            q = "\nMe: Do you guys want to {}? \n".format(a)
            print(q)
            """Adds the host question that starts the conversation to the record"""
            record.add(q)
