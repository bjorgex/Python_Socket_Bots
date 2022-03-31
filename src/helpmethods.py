import sys

import bots
import time

def getLocalIP():
    """
    Method to retunr your local IP address
    Source:
    https://www.delftstack.com/howto/python/get-ip-address-python/#use-the-socket-gethostname-function-to-get-the-local-ip-address-in-python
    :return:
    """
    import socket
    return socket.gethostbyname(socket.gethostname())

"""
Gets socket message from host/client decodes it and prints it out

"""


def getSocketMsg(_socket, BUFSIZE):
    try:
        get_msg = _socket.recv(BUFSIZE)  # Receives msg from host/client
    except ConnectionResetError:
        sys.exit("Couldn't connect to socket")
    else:
        msg = get_msg.decode('utf-8')  # Decodes msg
        return msg


"""
Sends message to a connected sockets
"""


def sendSocketMsg(_socket, msg):
    time.sleep(1)
    try:
        send_msg = msg.encode('utf-8')  # Encodes msg
    except ConnectionResetError:
        sys.exit("Couldn't connect to socket")
    else:
        _socket.send(send_msg)  # Sends msg from host/client


def yes_no(Yes_or_no):
    if Yes_or_no == "Yes":
        return True
    return False


"""
- Takes in a name of a bot as a string an calls that bots,
- with 2 actions
- Validate that the input string for the name has a bot method with the same name
"""


def callBot(botName, ac1, ac2):
    bot_to_call = getattr(bots, botName)
    if ac2 == "None":
        ac2 = None
    _response = bot_to_call(ac1, ac2)
    return _response


def doesSysArg3Exist():
    """
    This function is used for client.py script to get name
    :return:
    """
    try:
        arg1 = sys.argv[3]
    except IndexError:
        print("No arguments")
    else:
        return arg1
    return None


def isClientArgPosInt(clientNrArg):
    try:
        _clientNr = int(clientNrArg)
    except TypeError:
        print("Client number argument/input not an integer")
    else:
        if _clientNr < 0:
            print("Server only accepts numbers >= 0")
            return False
        else:
            return _clientNr
    return False


def isClientArgZero(isZero, thisFuncCalled):
    if isZero > 0:
        return False
    lonely_action = bots.__action__(1)
    lonely_suggestion = "Host: Would any of you want to {}?".format(lonely_action)
    print(lonely_suggestion)
    time.sleep(3)
    print("Any one there?")
    time.sleep(2)
    print("Wilson?")
    time.sleep(4)
    if thisFuncCalled >= 1:
        print("Did you really start a server for 0 clients again?...")
    else:
        print("Did you really start a server for 0 clients?...")

    time.sleep(2)
    print("This isn't fun, try asking for more than zero clients.")
    time.sleep(2)
    return True

