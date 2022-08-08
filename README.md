# Final Project: Communicate With Friends

Group: Simon Cao and David Ning

* __gui.py__: Use this file as the main module for the program. This contains all the buttons and user interfaces. This works closely with the __Final_Profile__ as it will pass parameter to the Final__Final_Profile__module, and use it to exchange data. Besides that, it also supports a night version, code inspired by https://www.youtube.com/watch?v=35V5r6S2_FA, Tkinter color tutorial. This module also takes care of left and right align of the text field. When message was sent from the user, it append a 0 to the message to add a flag indicating that it is the user sending to the recipient. Displaying the night version was inspired by StackOverflow, https://stackoverflow.com/questions/46602016/justifying-strings-left-and-right-in-tkinter-text-widget. At last, because we have to receive messages, we used threading, it runs every three seconds to check for new messages. Inspired by the website: https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds.
    In addition, we close threading when pressing x and close option, this is adapted from : https://stackoverflow.com/questions/49624631/how-to-change-the-function-of-x-button-of-a-tkinter-window-one-in-the-title.
    For the flourish, we did night mode which switches color.
    
    Because we don't want to overwork the server, we set it to three seconds.

* __client.py__: This module has a lot of functions that works with JSON formatted strings transfer through the web socket. It has join, respond, and other methods that allow the program to communicate with the server. This module links with the protocol module to recieve the datatuple that contains the information of server's return messages.

* __ds_messenger.py__: This module is the main connection with the server and port. It takes care of retriving and sending data to the server. gui.py will use a lot of this function to link it to the bottons for connection. This module will use client.py to send the formatted Json message to the server. It will use protocol to translate those return value and put them into a datatuple to give information.

* __Final_Profile.py__: This is an extension module from Profile module created by Professor Baldwin. We added two more classes that supports the need of our gui. A Class SaveData and a Class GetData. It also contains a single_double() method that was used ealier for A2 that turns single quotation to double quotation marks. This Module's SaveData Class have functions. Usually passing in the filename, username, recipient's username would be enought, depends on the parameter of the functions. This is used to be a data storage, it stores everything into a dsu file, the dsu file is owned by each user, it can contain different recipients and their messages. All the format is stored as JSON.
    For the delimiter splitting, the website that I used is:
    https://www.codegrepper.com/code-examples/python/python+split+without+removing+delimiter
    
* __protocol.py__: The protocol.py module gets the return Json string from the server and translate information into a datatuple that client.py module can do operations on.

* __test_ds_message_protocol.py__: This module is a test for the protocol. It calls for the server and receive messages for the protocol to be tested. It will check for multiple errors that might occur.

* __test_ds_messenger.py__: This module is a test that allows the developer to send in hardcoded username, password, and other parameter to test the functionality fo ds_messenger.
