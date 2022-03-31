#!/usr/bin/env python

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
import argparse
import math

arg_count = 0
if __name__ == "__main__":
    """
    Program arguments
        # Logic for how to handle the script arguments
        # Since we only want 1 argument we'll just check how many arguments is given
        # IF a user gives 2 arguments an error will occur 
        Source:
        https://realpython.com/python-command-line-arguments/
    """
    arg_count = len(sys.argv) - 1
    print(f"Arguments count: {arg_count}")

"""If there are no arguments like -h or an 'Integer', this if statement will be skipped"""
if arg_count > 0:
    """
    Argument description  
        # Lets you pass the argument --help,
        # to show you what other arguments you can use
        # in this script
        
        Source:
        https://stackoverflow.com/questions/9037828/writing-a-help-for-python-script
        ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
    """
    """Start of argument description"""
    parser = argparse.ArgumentParser(
        description='''My Description. This script only uses one optionoal argument''',
        epilog='''This is all the help you'll get''')
    parser.add_argument('INTEGER', type=int, default=42, help=''' 
        You can choose to enter a integer as an argument after the script name.
        This will decide how many clients that have to join, before the host
        starts looking for client names. Negative arguments will be transformed to positives''')
    args = parser.parse_args()
    """Argument description finished"""


def handler(signum, frame):
    """
    Traps
    # signal.SIGINT handles ctrl + c interrupts
    Source:
    https://code-maven.com/catch-control-c-in-python
    """
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)


signal.signal(signal.SIGINT, handler)


class ClientHandler(Thread):
    """
    ClientHandler class
    # Handles a client request.
    # Start threads for clients
    Source:
    Lecture 10 from DATA2410-V22
    """

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
            print("Client disconnected from handler")
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
        print(self._name + " is waiting for host")
        while True:
            """Waits for response from client"""
            _response = None
            try:
                _response = getSocketMsg(self._client, BUFSIZE)  # Receives message from bot
            except ConnectionAbortedError:
                print("Connection to client has been closed")
                break

            print("{}: {}".format(self._name, _response))
            if not _response:
                print("Client disconnected")
                connected_clients.remove(self._client)
                self._client.close()
                break
            else:
                _response = self._name + ' ' + ctime() + ': \n' + _response
                self._record.add(_response)
                hostRecord.add(_response)
                self._client.send(str(self._record).encode('utf-8'))


"""
Creating hosts server
"""
HOST = 'localhost'                      # Initialize server address
PORT = 5000                             # Initialize server port
ADDRESS = (HOST, PORT)                  # Puts address and port together
BUFSIZE = 1024                          # The block size in bytes
hostRecord = ChatRecord()               # Initialize the host record
record = ChatRecord()                   # Initialize the record that the clients are going to use
server = socket(AF_INET, SOCK_STREAM)   # Create a socket server with TCP protocol
server.bind(ADDRESS)                    # Binds the host address and port number to the socket

"""
Handles sys.arg for client number
    # If there are sys.arg for client number,
    # clientNrRoof should equal that sys.arg
    # It also handles negative arguments and turns the them into positives
"""
clientNrRoof = False
choose_zero_clients = 0
if arg_count > 0:
    arg1 = int(sys.argv[1])  # Finds the absolute value of cl
    arg1_abs = int(math.sqrt(arg1 ** 2))
    clientNrRoof = arg1_abs
    if isClientArgZero(clientNrRoof, choose_zero_clients):
        clientNrRoof = False

""" 
Handles user input for clientNrRoof when there is no sys.arg or sys.arg was 0
"""
while not clientNrRoof:
    _inputArg = "How many clients has to connect before the chat room host suggests something?: "
    clientNrRoof = isClientArgPosInt(input(_inputArg))  # Checks if user input is a positive integer
    _isZero = isClientArgZero(clientNrRoof, choose_zero_clients)  # Checks if clientNrRoof is zero
    if _isZero:
        clientNrRoof = False

# Only positive numbers under here
print("Waiting for {} clients...".format(clientNrRoof))
server.listen(clientNrRoof+4)  # Que up to clientNrRoof
connected_clients = []  # List of all connected clients
clientNamesReceived = []  # List of all client names received
_round = 0  # Initialize variable
"""
The server now waits for connections from clients,
and hands sockets off to clients handlers
"""
while True:
    """Gather clientNrRoof of clients"""
    print('Waiting for connections...')
    print("There is " + str(len(connected_clients)) + " connected clients")
    client, address = server.accept()
    print('... connected from: ', address)
    handler = ClientHandler(client, record)
    handler.start()
    time.sleep(1)
    connected_clients.append(client)  # Appends client names to connected clients

    """Steps into while loop when connected clients have reached clientNrRoof"""
    while len(connected_clients) == clientNrRoof:
        print("Enough clients have joined the chat room \n")
        print("Retrieving bot names...")

        """Steps out of loop when clientNameReceived has reached clientNrRoof"""
        while len(clientNamesReceived) != clientNrRoof:
            """Loops around until client names are received"""
            print("Need to retrieve", clientNrRoof - len(clientNamesReceived),
                  "more bot names")
            time.sleep(2)
            if not len(clientNamesReceived) < clientNrRoof:
                break

        print("\nAll names received")
        print("Sending suggestion")
        _rand = random.choice([1, 2])  # Picks either one or two actions, if _rand = 1 --> _action2 = "None"
        if _rand == 1:
            _action1 = __action__(1)  # Gets 1 action
            _action2 = "None"  # Sets action2 to "None"
            _suggestion = "Host: Would any of you want to {}?".format(_action1)  # Create suggestion
            print("Action1: {}\nAction2: None".format(_action1))
        else:
            _action1, _action2 = __action__(2)  # Gets 2 actions
            _suggestion = "Would any of you want to {}? Or maybe {}?".format(_action1, _action2)  # Create suggestion
            print("Actions1: {}\nAction2: {}".format(_action1, _action2))

        """A new round starts here"""
        _round = _round + 1  # Adds a round to variable _round
        print("\nRound ", _round, " starts now!\n-----------------------------------")
        print("Host: {}".format(_suggestion))
        hostRecord.add(_suggestion)       # Adds suggestion to hostRecord
        for client in connected_clients:  # Sends the suggestion and actions from host to clients
            sendSocketMsg(client, _suggestion)
            sendSocketMsg(client, _action1)
            sendSocketMsg(client, _action2)

        time.sleep(3)  # Waits for 5 seconds to make sure that all the Threads have received their data
        """Prints out record"""
        print("\nHost record:.............\n"
              "{}"
              "\nEnd of Record....................\n".format(hostRecord))
        """"Asks host if they want to start a new round or quit the server"""
        while True:
            _choise = input("New round(R)? - Quit server(Q)?\n"
                            "Write either R or Q here to choose: ")
            if _choise == "R":
                break
            elif _choise == "Q":
                for client in connected_clients:
                    sendSocketMsg(client, "Q")
                    #client.close()
                    client.detach()
                    time.sleep(1)
                server.close()
                sys.exit("Quit chat bot")
            else:
                print("Error: Wrong input, try again!")


