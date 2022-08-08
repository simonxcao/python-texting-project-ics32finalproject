import socket
from client import *


def send_msg(server: str, port: int, username: str, password: str, message=None, recipient=None):
    """
      The send function joins a ds server and sends a message, bio, or both

      :param server: The ip address for the ICS 32 DS server.
      :param port: The port where the ICS 32 DS server is accepting connections.
      :param username: The user name to be assigned to the message.
      :param password: The password associated with the username.
      :param message: The message to be sent to the server.
      :param recipient: Optional, a recipient string for the program to use.
    """
    try:
        # creates the socket and connects to the server and port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # shorten wait time to 5 seconds if server or port is unresponsive
        sock.settimeout(5)
        sock.connect((server, port))
        connection = init(sock)

        # sends the join JSON format to the server
        write_msg(connection, join(username, password))
        server_msg = read_msg(connection)
        t = extract_json(server_msg)
        print(t.response['message'] + '\n')
        # extracts the token from the response message from the server
        toke = t.response['token']
        write_msg(connection, direct_message(message, recipient, toke))
        server_msg = read_msg(connection)
        respond(server_msg)
        # closes the writing and receiving file objects
        disconnect(connection)
        return True

    # catches all the errors that might arise in the function
    except ds_error:
        print("An error occurred while attempting to communicate with the server.")
        return False
    except ConnectionRefusedError:
        print("An error occurred while attempting to communicate with the server.")
        return False
    except OSError:
        print("An error occurred while attempting to communicate with the server.")
        return False
    except KeyError:
        print("An error occurred while attempting to communicate with the server.")
        return False
    except Exception as e:
        print(e)
        return False

    finally:
        # closes the socket
        sock.close()


def request_msg(server: str, port: int, username: str, password: str):
    """This function use socket to connect and then get the json message from the server."""
    try:
        # creates the socket and connects to the server and port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # shorten wait time to 5 seconds if server or port is unresponsive
        sock.settimeout(5)
        sock.connect((server, port))
        connection = init(sock)

        # sends the join JSON format to the server
        write_msg(connection, join(username, password))
        server_msg = read_msg(connection)
        t = extract_json(server_msg)
        print(t.response['message'] + '\n')
        # extracts the token from the response message from the server
        toke = t.response['token']
        # requests unread messages
        write_msg(connection, new_msg(toke))
        server_msg = read_msg(connection)
        respond1(server_msg)

        # requests all messages
        write_msg(connection, all_msg(toke))
        server_msg = read_msg(connection)
        respond1(server_msg)


        # closes the writing and receiving file objects
        disconnect(connection)
        return True

    # catches all the errors that might arise in the function
    except ds_error:
        print("An error occurred while attempting to communicate with the server.")
        return False
    except ConnectionRefusedError:
        print("An error occurred while attempting to communicate with the server.")
        return False
    except OSError:
        print("An error occurred while attempting to communicate with the server.")
        return False
    except KeyError:
        print("An error occurred while attempting to communicate with the server.")
        return False
    except Exception as e:
        print(e)
        return False

    finally:
        # closes the socket
        sock.close()


if __name__ == '__main__':
    send_msg('168.235.86.101', 3021, 'GULLY', 'okcool', 'Hello', 'Ging')  # Hardcoded tests
    request_msg('168.235.86.101', 3021, 'Ging', 'okokok')
    send_msg('168.235.86.101', 3021, 'GULLY', 'okcool', 'Loser', 'Ging')
    request_msg('168.235.86.101', 3021, 'Ging', 'okokok')