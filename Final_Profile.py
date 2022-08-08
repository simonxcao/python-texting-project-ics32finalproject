# Profile.py
# ICS 32 Winter 2022
# Final Project
# Author: Mark S. Baldwin
# Modified by David Ning and Simon Cao
# tcao10 @ uci.edu, zhenglin @uci.edu
# v0.1.8

import json, time, os
from pathlib import Path


def single_double(jsonFile):
    """Change to single quotation to double quatation mark"""
    x = ""
    determine = False

    for i in jsonFile:
        if i == "'" and not determine:
            i = '"'  # Replace single to double quotation mark
        elif i == "'" and determine:
            x = x[:-1]  # Remove x before single quotes
        elif i == '"':
            i = '\\' + i  # x has double quotes
        determine = (i == "\\")  # See if determine should be True or False
        x += i
    return x


class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to load or save Profile objects to file the system.
    """
    pass


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to deserialize a dsu file to a Profile object.
    """
    pass


class Post(dict):
    """
    The Post class is responsible for working with individual user posts. It currently supports two features:
    A timestamp property that is set upon instantiation and when the entry object is set and an
    entry property that stores the post message.
    """

    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry

    def set_time(self, time: float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        return self._timestamp

    """
    The property method is used to support get and set capability for entry and time values.
    When the value for entry is changed, or set, the timestamp field is updated to the
    current time.
    """
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32 DSU server. You will need to
    use this class to manage the information provided by each new user created within your program for a2.
    Pay close attention to the properties and functions in this class as you will need to make use of
    each of them in your program.

    When creating your program you will need to collect user input for the properties exposed by this class.
    A Profile class should ensure that a username and password are set, but contains no conventions to do so.
    You should make sure that your code verifies that required properties are set.
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''  # OPTIONAL
        self._posts = []  # OPTIONAL

    def add_post(self, post: Post) -> None:
        """
        add_post accepts a Post object as parameter and appends it to the posts list. Posts are stored in a
        list object in the order they are added. So if multiple Posts objects are created, but added to the
        Profile in a different order, it is possible for the list to not be sorted by the Post.timestamp property.
        So take caution as to how you implement your add_post code.
        """
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        """
        del_post removes a Post at a given index and returns True if successful and False if an invalid
        index was supplied.

        To determine which post to delete you must implement your own search operation on the posts
        returned from the get_posts function to find the correct index.
        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        """
        get_posts returns the list object containing all posts that have been added to the Profile object
        """
        return self._posts

    """

    save_profile accepts an existing dsu file to save the current instance of Profile to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError

    """

    def save_profile(self, path: str) -> None:
        """save_profile accepts an existing dsu file to save the current instance of Profile to the file system."""
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored in a DSU file.

    Example usage: 

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """

    def load_profile(self, path: str) -> None:
        """load_profile will populate the current instance of Profile with data stored in a DSU file."""
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()


class SaveData:
    """This class saves the data locally in dsu files"""
    def __init__(self):
        self.username = None
        self.re_username = None
        self.password = None
        self.dsuserver = None
        self.message_list = []

    def add_post(self, post: Post) -> None:
        """Add post into the message_list"""
        self.message_list.append(post)  # Adding post to the message_list list

    def check_for_duplicate(self, re_username, filename):
        """This method checks for the duplicated recipient's username in the dsu file"""
        opener = open(filename, 'r')  # Open the file first
        read = opener.readlines()  # Read the lines in the file
        if read == [] or read == '\n':
            return False  # Return False
        else:
            delimiter = "{"  # Sets up the delimiter, but append it
            s = [delimiter + e for e in read[0].split(delimiter) if e]  # Split the string into sections
            return_return = None
            for i in s:  # If the recipient is found
                x = json.loads(i)
                if x['re_username'] == re_username:  # Check if it contains the recipient's username
                    return True  # Send back true
                else:
                    return_return = False
            return return_return

    def load_profile(self, re_username, filename):
        """Load the profile and split the string"""
        try:  # Split them apart first
            f = open(filename, 'r')
            reader = f.readline()
            delimiter = "{"  # Sets up the delimiter, but append it
            s = [delimiter + e for e in reader.split(delimiter) if e]  # Split the string into sections
            # line 247 Adapted from codegrepper.com
            flag = 0  # Flag is for the wanted recipient
            for i in s:
                if eval(i)['re_username'] == re_username:  # If the dictionary's username is the username we want
                    s.remove(i)  # Remove from the dictionary
                    flag = i

            self.username = eval(flag)['username']  # Turn flag to a dictionary using eval() then get the username
            self.re_username = eval(flag)['re_username']
            self.password = eval(flag)['password']
            self.dsuserver = eval(flag)['dsuserver']
            for post_obj in eval(flag)['message_list']:
                self.message_list.append(post_obj)
            return s  # Return the removed list

        except Exception as ex:
            print(ex)
            raise DsuProfileError(ex)

    def save_into_dsu(self, username, message, re_username, password, dsuserver, filename) -> None:
        """This method gets all the parameter and is most likely the entry point of this SaveData()"""
        checker = self.check_for_duplicate(re_username, filename)  # Go check it the recipient was made
        if checker is False:  # If return value is false, it means it does not exist
            try:
                f = open(filename, 'a')  # Add to the file
                self.dsuserver = dsuserver
                self.username = username
                self.re_username = re_username
                self.password = password
                self.message_list.append(message)
                json.dump(self.__dict__, f)  # Dump it into the file with JSON format
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            current_remove = self.load_profile(re_username, filename)  # Get the rest of the information (without the current user one)
            f = open(filename, 'w')  # Delete everything inside the file
            f.close()
            self.add_post(message)  # Add post to the current user's list
            f = open(filename, 'a')  # Overwrite the current string inside the file
            if len(current_remove) != 0:
                for i in current_remove:
                    x = str(i)
                    f.write(x)  # Append the original into the file
                y = self.__dict__
                new_insert = single_double(str(y))  # Make sure it is double quotation mark
                f.write(new_insert)  # Insert the new message
                f.close()
            else:
                x = self.__dict__
                new_insert = single_double(str(x))  # Double quotation
                f.write(new_insert)
                f.close()

    def open_mes(self, filename):
        """This method accepts a filename and return a list of recipient"""
        opener = open(filename, 'r')
        reader = opener.readline()
        delimiter = "{"  # Split the information
        s = [delimiter + e for e in reader.split(delimiter) if e]  # Split the string into sections
        return_list = []
        for i in s:
            res = json.loads(i)
            return_list.append(res['re_username'])  # Get the recipient username into a list
        return return_list

    def re_message_get(self, re_username, filename):
        """This method gets a recipient's username and filename, it returns a list of all the messages"""
        opener = open(filename, 'r')
        reader = opener.readline()
        delimiter = "{"
        s = [delimiter + e for e in reader.split(delimiter) if e]  # Split the string into sections
        return_list = []
        for i in s:
            res = json.loads(i)  # Load the data (in Json)
            if re_username == res['re_username']:  # Get the recipient's username
                for j in res['message_list']:
                    if j == []:
                        return None  # Empty file
                    else:
                        return_list.append(j)  # Append all the messages
        return_list.remove(return_list[0])  # Remove the first item because it is always an empty ''
        return return_list

    def return_user_pass(self, filename):
        """This method takes in a filename and return a list of user's information such as username, password, and dsuserver"""
        opener = open(filename)
        reader = opener.readline()
        delimiter = "{"
        s = [delimiter + e for e in reader.split(delimiter) if e]  # Split the string into sections
        return_list = []  # Create an empty list
        for i in s:
            res = json.loads(i)  # Load all the information in Json
            return_list.append(res['username'])
            return_list.append(res['password'])
            return_list.append(res['dsuserver'])
            break  # Because it does not need to run multiple times, all the above variables are the same for all.
        return return_list


class GetData:
    """This class gets the data from local dsu file, and return a list of information"""
    def __init__(self):
        self.filename = None
        self.dsuserver = None
        self.username = None
        self.password = None
        self.bio = None
        self.message_list = []

    def get_file_name(self):
        """Ask for the input of the file's name"""
        self.filename = input("Enter the path of the dsu file")  # Want the filename from the user

    def send_file(self, message) -> list:
        """Take in message as a parameter and get the items"""
        message = json.loads(message)
        self.dsuserver = message['dsuserver']
        self.username = message['username']
        self.password = message['password']
        self.bio = message['bio']
        profile = Profile()  # Open the profile
        profile.load_profile(self.filename)
        x = profile.get_posts()  # Get all the posts
        y = str(x)
        getter = single_double(y)
        count = y.split('}, {')  # Split the string.
        g = len(count)
        alist = json.loads(getter)  # Load the json file
        if g != 1:
            for i in range(g):
                self.message_list.append(alist[i]["entry"])  # Print out the element in the json file
        else:
            print("no post")
        return_list = [self.dsuserver, self.username, self.password, self.bio, self.message_list]  # Return info list
        return return_list
