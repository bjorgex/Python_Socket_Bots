from socket import *

"""
Try sending bytes to server 3 time, 
if not successful we'll consider the connection cut off.
"""


def valEstasblishedConnection(_server, _clientNr):
    print("Start of connection validation for client{}...".format(_clientNr))
    _tries = 1
    while _tries <= 3:

        try:
            msg = "Connection to server is still reliable"
            sendSocketMsg(_server, msg)
        except:
            _tries = ++1
            print("Method failed to send over bytes")
            print("Try # " + str(_tries))
        else:
            print("Bytes reached server")
            """Returns the function with a boolean value True"""
            return True
    """Try fails 3 times Function returns false"""
    return False


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
