from socket import *

"""
Gets socket message from host/client decodes it and prints it out

"""
def getSocketMsg(_socket, BUFSIZE):
    get_msg = _socket.recv(BUFSIZE)     # Receives msg from host/client
    msg = get_msg.decode('utf-8')       # Decodes msg
    print(msg)                          # Prints msg


"""
Sends message to a connected sockets
"""
def sendSocketMsg(_socket, msg):
    send_msg = msg.encode('utf-8')      # Encodes msg
    get_msg = _socket.send(send_msg)    # Sends msg from host/client

"""Yes or now boolean method"""

def yes_no(Yes_or_no):
    if Yes_or_no == "Yes":
        return True
    return False

