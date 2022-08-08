# Simon Cao & David Ning

import socket
import json, time
import client
import protocol


class DirectMessage:
    """
    Class that takes in the recipient and the message that is going to be send to the recipient
    """
    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message
        self.timestamp = time.time()


class DirectMessenger:
    """
    Class that handles the communication with the server
    """
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None

    def send(self, message: str, recipient: str) -> bool:
        """
        Method that sends the message to the recipient
        """

        try:
            # creates the socket and connects to the server and port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # shorten wait time to 5 seconds if server or port is unresponsive
            sock.settimeout(5)
            sock.connect((self.dsuserver, 3021))
            connection = client.init(sock)

            # sends the join JSON format to the server
            client.write_msg(connection, client.join(self.username, self.password))
            server_msg = client.read_msg(connection)
            t = protocol.extract_json(server_msg)
            print(t.response['message'] + '\n')
            # extracts the token from the response message from the server
            toke = t.response['token']
            self.token = toke
            # sends the message to the recipient
            client.write_msg(connection, client.direct_message(message, recipient, self.token))
            server_msg = client.read_msg(connection)
            client.respond(server_msg)
            # closes the writing and receiving file objects
            client.disconnect(connection)
            return True
        # catches all the errors that might arise in the function
        except client.ds_error:
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


    def retrieve_new(self) -> list:
        """
        Method that retrieves all new messages that's sent to this user and returns a list of DirectMessage objects containing all new messages
        """
        try:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # shorten wait time to 5 seconds if server or port is unresponsive
            sock.settimeout(5)
            sock.connect((self.dsuserver, 3021))
            connection = client.init(sock)

            # sends the join JSON format to the server
            client.write_msg(connection, client.join(self.username, self.password))
            server_msg = client.read_msg(connection)
            t = protocol.extract_json(server_msg)
            print(t.response['message'] + '\n')
            toke = t.response['token']

            # requests unread messages
            client.write_msg(connection, client.new_msg(toke))
            server_msg = client.read_msg(connection)
            client.disconnect(connection)

            # returns list with all the unread messages
            return protocol.extract_lots(server_msg)

        # catches the exceptions
        except client.ds_error:
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
            # close socket
            sock.close()

    def retrieve_all(self) -> list:
        """
        Method that retrieves all the messages that were ever sent to this user
        """
        try:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # shorten wait time to 5 seconds if server or port is unresponsive
            sock.settimeout(5)
            sock.connect((self.dsuserver, 3021))
            connection = client.init(sock)

            # sends the join JSON format to the server
            client.write_msg(connection, client.join(self.username, self.password))
            server_msg = client.read_msg(connection)
            t = protocol.extract_json(server_msg)
            print(t.response['message'] + '\n')
            toke = t.response['token']

            # requests all messages
            client.write_msg(connection, client.all_msg(toke))
            server_msg = client.read_msg(connection)
            client.disconnect(connection)

            # returns a list of DirectMessage objects containing all new messages
            return protocol.extract_lots(server_msg)

        # catches all exceptions
        except client.ds_error:
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
            sock.close()
