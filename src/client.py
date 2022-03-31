#!/usr/bin/env python
import argparse
import signal
from socket import *
from helpmethods import *
import sys
"""
The client will do the following:
1. Create a TCP socket and connect to (ip, port)
"""

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
    parser.add_argument('IP', type=str, default=42, help='''
    This argument takes an IP address like for exampler: 192.168.30.172.''')
    parser.add_argument('PORT', type=int, default=42, help='''
    This argument takes an PORT number in 0-65535, but preferably use 5000 adn up''')
    parser.add_argument('Bot name', type=str, default=42, help=''' 
        You can choose to enter a name of one the bots that the client have as an argument after the script name.
        This will decide which bot that corresponds to this client''')
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
IP = sys.argv[1]
HOST = IP
PORT = int(sys.argv[2])
ADDRESS = (HOST, PORT)
print("Host socket: {}".format(ADDRESS))
BUFSIZE = 1024*2
c = socket(AF_INET, SOCK_STREAM)  # TCP socket for IPv4

has_name = False
failed_attempts = 0
_bots = ["alice", "bob", "dora", "chuck"]
print("Choose between theese bots: {}".format(_bots))
name = doesSysArg3Exist()
print(name)
while True:
    for bot in _bots:
        if bot == name:
            has_name = True
            break
    if has_name:
        break
    else:
        failed_attempts = failed_attempts + 1
        name = input("Whatcha name dude??")

    if failed_attempts > 3:
        print("To many failed attempts, closing client connection to server")
        c.close()
        break
# End of loop

try:
    c.connect(ADDRESS)  # Connects to host server and added in a list of connected clients
except ConnectionRefusedError:
    sys.exit("Could not connect to host server")
welcome_msg = getSocketMsg(c, BUFSIZE)  # Get welcome msg
print(welcome_msg)

while True:
    if has_name:
        sendSocketMsg(c, name)  # Sends name to host

        while True:
            """Wait fro record list"""
            print("Waiting for record")
            record = c.recv(BUFSIZE)  # Receives a record list, should say no messages yet when first recieved
            if not record:
                print("Server disconnected because of not receiving record")
                break
            print("\nPrint Record:...........\n{}\nPrint record end...........\n".format(record.decode('utf-8')))
            print("Waiting for suggestion")
            try:
                _suggestion = getSocketMsg(c, BUFSIZE)  # Get suggestion
            except ConnectionResetError:
                sys.exit("Could not connect to host server, closing client")
            if _suggestion == "Q":
                print("Server disconnected because it received a 'Q' from host")
                break
            if not _suggestion:
                print("Server disconnected from host")
                break

            print("\nPrint suggestion: ")
            print(_suggestion)
            _action1 = getSocketMsg(c, BUFSIZE)
            print("Action1 got: {}".format(_action1))
            _action2 = getSocketMsg(c, BUFSIZE)
            print("Action2 got: {}".format(_action2))

            _response = callBot(name, _action1, _action2)  # Call bot, the bot will
            print("\nPrint response: ")
            print(_response)
            sendSocketMsg(c, _response)  # Send responds to host

        c.close()
        break
    break
