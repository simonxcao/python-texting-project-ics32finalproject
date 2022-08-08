# Simon Cao & David Ning
# tcao10@uci.edu
# 85427485


from protocol import extract_json, extract_lots
from collections import namedtuple
import json, time


class ds_error(Exception):
    """
    Custom class to handle exceptions
    """
    # handles all the exceptions that happens in the program
    pass


# namedtuple that contains the socket, writing file, and reading file
Connection = namedtuple('Connection', ['socket', 'writing', 'recv'])


def init(sock):
    """
    Function for creating file objects to handle input and output.
    """
    try:
        fsend = sock.makefile('w')
        freceiv = sock.makefile('r')

    except:
        raise ds_error

    # returns a namedtuple
    return Connection(socket=sock, writing=fsend, recv=freceiv)


def disconnect(tuples):
    """
    Function responsible for closing the file objects
    """
    tuples.writing.close()
    tuples.recv.close()


def join(user, passwd):
    """
    Function responsible for returning the JSON format for joining the server in a string type
    """
    x = {"join": {"username": user, "password": passwd, "token": ""}}
    return json.dumps(x)


def write_msg(tuples, msg):
    try:
        tuples.writing.write(msg + '\n')
        # makes sure everything is sent
        tuples.writing.flush()
    except:
        raise ds_error


def read_msg(tuples):
    """
    Function responsible for receiving the output from the server
    """
    return tuples.recv.readline()


def posting(msg, key):
    """
    Function responsible for returning the JSON format for when posting a message to the server
    """
    x = {"token": key, "post": {"entry": msg, "timestamp": time.time()}}
    return json.dumps(x)


def direct_message(msg, usr, key):
    """
    Function responsible for sending direct message
    """
    x = {"token": key, "directmessage": {"entry": msg, "recipient": usr, "timestamp": time.time()}}
    return json.dumps(x)


def new_msg(key):
    """
    Function responsible for sending in a request to retrieve new messages
    """
    x = {"token": key, "directmessage": "new"}
    return json.dumps(x)


def all_msg(key):
    """
    Function responsible for sending in a request to retrieve all messages
    """
    x = {"token": key, "directmessage": "all"}
    return json.dumps(x)


def respond(msg):
    """
    Function responsible for printing out the message in the response string from the server
    """
    try:
        t = extract_json(msg).response['message']
        print(t + '\n')
    except:
        raise ds_error


"""
Function responsible for retrieving new and all messages
"""


def respond1(msg):
    try:
        t = extract_lots(msg)
        print(t)
    except:
        raise ds_error
