# ds_protocol.py

# Starter code for Final in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Simon and David
# tcao10 @uci.edu, zhenglin @uci.edu

import json
from collections import namedtuple


# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['response'])


def extract_json(json_msg: str) -> DataTuple:
    """Call the json.loads function on a json string and convert it to a DataTuple object"""
    try:
        json_obj = json.loads(json_msg)
        # gets the dictionary in the server return message
        info = json_obj['response']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(info)


def extract_lots(json_msg: str) -> list:
    """This function returns a list of messages decoded using json"""
    try:
        info = []
        json_obj = json.loads(json_msg)  # Load all the messages
        resp = json_obj['response']['messages']
        for x in resp:
            info.append(x)  # append to the list
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    return info

