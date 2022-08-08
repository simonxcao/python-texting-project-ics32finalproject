# Simon Cao & David Ning
from ds_messenger import DirectMessenger, DirectMessage


# test for the classes created in ds_messenger
if __name__ == '__main__':
    jose = DirectMessage('Jose', "Ok buddy")
    print(jose.timestamp)
    simon = DirectMessenger('168.235.86.101', 'Lice', "coolio")

    simon.send(jose.message, jose.recipient)
    jose1 = DirectMessenger('168.235.86.101', 'Jose', "LOOOOOOOOL")
    print(jose1.retrieve_new())




