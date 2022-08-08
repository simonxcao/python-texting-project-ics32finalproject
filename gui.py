# Simon Cao & David Ning
# tcao10@uci.edu
# 85427485


import tkinter as tk
from tkinter import ttk, filedialog
from Final_Profile import Post, Profile, SaveData
import ds_messenger as ms
import time
from threading import Event, Thread

# variables to add to Profile instances
USER = 'Billybob12'
PASS = 'kkkookkokokokook'
SERVER = '168.235.86.101'



class RepeatedTimer:

    """Repeat `function` every `interval` seconds. Adapted from stackoverflow for stopping threading"""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()


class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self._file = None

        # a list of the recipients available in the active DSU file
        self._messages = []
        self._recipient = None

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance
        self._draw()


    def node_select(self, event):
        """
        Method for selecting object on treeview and loading the past messages from this recipient into the text widget
        """
        self.entry_editor.configure(state='normal')
        self.entry_editor.delete(0.0, 'end')
        self.entry_editor.insert(0.0, '')

        index = int(self.posts_tree.selection()[0])
        entry = self._messages[index]
        # sets the data attribute as the name of the recipient
        self._recipient = entry

        x = SaveData()
        # gets list of message that has occurred between the user and the recipient
        mess = x.re_message_get(self._recipient, self._file)
        if mess is None:
            pass
        else:
            try:
                # loads in the texts depending on if they are the users or the recipients
                for x in mess:
                    if x[-1] == '1':
                        mes = x[:-1]
                        self.entry_editor.insert('end', mes + '\n', 'left')
                    elif x[-1] == '0':
                        mes = x[:-1]
                        self.entry_editor.insert('end', mes + '\n', 'right')
                    else:
                        pass
            except IndexError:
                pass
        # return the text widget to read only
        self.entry_editor.configure(state='disabled')


    def reset_ui(self):
        """
        Method that resets the treeview and the text widget
        """
        self.entry_editor.configure(state='normal')
        self.entry_editor.delete(0.0, 'end')
        self.entry_editor.insert(0.0, '')
        self.entry_editor.configure(state='disabled')
        self._messages = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)


    def set_posts(self, name: list):
        """
        Method that imports all the recipients in the DSU file into the treeview accoridng to their order
        """
        self._messages = name
        for i in range(len(self._messages)):
            self._insert_post_tree(i, self._messages[i])

    def get_text(self):

        """
        Method that gets the message that user want to send to a recipient
        """
        return self.send_stuff.get('1.0', 'end').rstrip()



    def set_text(self, text):
        """
        Method that clears the text widget after the user clicks the send button
        """
        self.send_stuff.delete(0.0, 'end')
        self.send_stuff.insert(0.0, text)


    def insert(self, name):
        """
        Method that inserts a recipient that's added by the add button into the treeview
        """
        self._messages.append(name)
        id = len(self._messages) - 1
        self._insert_post_tree(id, name)



    def _insert_post_tree(self, id, name):
        """
        Method that adds to the treeview
        """
        label = name
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        self.posts_tree.insert('', id, id, text=label)


    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        # treeview widget and frame
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        # disable the text widget to make it read only
        self.entry_editor = tk.Text(editor_frame, state='disabled', width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

        # configures the texts in the text widget so that we can make a text appear on the left or right
        # lines 191-192 adapted by stackoverflow on how to display text to the left or right
        self.entry_editor.tag_configure("right", justify="right")
        self.entry_editor.tag_configure("left", justify="left")

        # second text widget that is for the user to enter stuff
        entry_frame2 = tk.Frame(master=self, bg="")
        entry_frame2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame2 = tk.Frame(master=entry_frame2, bg="red")
        editor_frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.send_stuff = tk.Text(master=editor_frame2, width=0)
        self.send_stuff.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)





class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, send_callback=None, add_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        # sets data attributes with the parameters
        self._send_callback = send_callback
        self._add_callback = add_callback

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance
        self._draw()


    def send_click(self):
        """
        Calls the callback function specified in the send_callback class attribute, if
        available, when the send_button has been clicked.
        """

        if self._send_callback is not None:
            self._send_callback()


    def add_click(self):
        """
        Calls the callback function specified in the add_callback class attribute, if
        available, when the add_button widget has been clicked.
        """
        if self._add_callback is not None:
            self._add_callback()


    def disable(self):
        """
        Disables the send and add button if nothing is created or opened
        """
        self.send_button["state"] = "disabled"
        self.add_button["state"] = "disabled"



    def enable(self):
        """
        Enables the send and add button after a file is created or opened
        """
        self.send_button["state"] = "active"
        self.add_button["state"] = "active"



    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        # send button
        self.send_button = tk.Button(master=self, text="Send", width=20)
        self.send_button.configure(command=self.send_click)
        self.send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        # add user button
        self.add_button = tk.Button(master=self, text="Add User", width=10)
        self.add_button.configure(command=self.add_click)
        self.add_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

        # disables the buttons
        self.disable()



class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the Profile class.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._profile_filename = None

        # Initialize a new Profile and assign it to a class attribute.
        self._current_profile = Profile()

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()



    def new_profile(self):
        """
        Creates a new DSU file when the 'New' menu item is clicked.
        """
        try:
            filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
            self._profile_filename = filename.name
            self.body._file = self._profile_filename

            # enables the buttons
            self.footer.enable()

            self._current_profile = Profile()
            # assigns the default values to these data attributes
            self._current_profile.username = USER
            self._current_profile.password = PASS
            self._current_profile.dsuserver = SERVER
            self.body.reset_ui()

            # calls the function that automatically retrieves messages
            # creates repeatedtimer object
            rt = RepeatedTimer(2.5, self.new_msg)
            self.control = rt


        except Exception as e:
            print(e)


    def open_profile(self):
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI.
        """
        try:
            # reset treeview and entry widget when it is called
            self.body.reset_ui()

            filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
            self._profile_filename = filename.name
            self.body._file = self._profile_filename

            # enables the buttons
            self.footer.enable()

            self._current_profile = Profile()

            x = SaveData()
            y = x.return_user_pass(self._profile_filename)
            # gets the user, pass, dsuserver from the DSU file
            self._current_profile.username = y[0]
            self._current_profile.password = y[1]
            self._current_profile.dsuserver = y[2]

            # imports the messages into the treeview
            self.body.set_posts(x.open_mes(self._profile_filename))
            # calls the function that automatically retrieves new messages
            # creates repeatedtimer object
            rt = RepeatedTimer(2.5, self.new_msg)
            self.control = rt


        except Exception as e:
            print(e)


    def save_profile(self):
        """
        Method that sends the direct message once the send button is clicked and also saves it to the dsu file
        """
        # makes sure user can't send in empty messages or whitespaces
        if len(self.body.get_text()) == 0 or self.body.get_text().isspace() is True:
            pass
        else:
            # makes sure a user selected a recipient to talk to
            if self.body._recipient is None:
                print('select user to talk to')
            else:
                message = self.body.get_text()

                # creates instances of the classes
                exchange = ms.DirectMessage(self.body._recipient, message)
                more = ms.DirectMessenger(self._current_profile.dsuserver, self._current_profile.username,
                                          self._current_profile.password)
                # makes sure the send method worked
                if more.send(exchange.message, exchange.recipient) is True:

                    # inserts the text into the read only text widget once the send button is clicked
                    self.body.set_text("")
                    self.body.entry_editor.configure(state='normal')
                    self.body.entry_editor.insert('end', message + '\n', 'right')
                    self.body.entry_editor.configure(state='disabled')

                    # stores the text into the DSU file
                    message = message + '0'
                    x = SaveData()
                    x.save_into_dsu(self._current_profile.username, message, self.body._recipient,
                                    self._current_profile.password, self._current_profile.dsuserver,
                                    self._profile_filename)
                    self.body.set_text("")
                else:
                    print('issue occurred with server or network')


    def new_msg(self):
        """
        Method that keeps connecting to the server every 3 seconds to receive new messages that might be sent
        """
        try:
            exchange = ms.DirectMessenger(self._current_profile.dsuserver, self._current_profile.username,
                                          self._current_profile.password)
            # gets list of all new messages
            list1 = exchange.retrieve_new()

            # makes sure there is new messages
            if len(list1) > 0:
                for x in list1:
                    # checks if the user has clicked on a treeview item yet
                    if self.body._recipient is not None:

                        # checks if the message that's sent is from the recipient they clicked on
                        if x['from'] == self.body._recipient:
                            # inserts the message to the read only text widget
                            self.body.entry_editor.configure(state='normal')
                            self.body.entry_editor.insert('end', x['message'] + '\n', 'left')
                            self.body.entry_editor.configure(state='disabled')
                            # saves message to the DSU file
                            message = x['message'] + '1'
                            x = SaveData()
                            x.save_into_dsu(self._current_profile.username, message, self.body._recipient,
                                            self._current_profile.password, self._current_profile.dsuserver,
                                            self._profile_filename)
                        # if the message that's sent is not from the recipient they clicked on
                        else:
                            message = x['message'] + '1'
                            l = x['from']
                            x = SaveData()
                            x.save_into_dsu(self._current_profile.username, message, l,
                                            self._current_profile.password, self._current_profile.dsuserver,
                                            self._profile_filename)
                    # if the user has not clicked on a recipient yet
                    else:
                        message = x['message'] + '1'
                        l = x['from']
                        x = SaveData()
                        x.save_into_dsu(self._current_profile.username, message, l,
                                        self._current_profile.password, self._current_profile.dsuserver,
                                        self._profile_filename)

            else:
                pass
        except:
            print('Something occurred with the server and network')



    def close(self):
        """
        Closes the program when the 'Close' menu item is clicked.
        """
        self.root.destroy()
        self.control.stop()


    def add(self):
        """
        Method that runs when the add button is clicked
        """
        # add user to the tree
        top = tk.Toplevel()
        top.title('Add User')
        user = tk.Label(top, text="Add Contact:")
        user.pack(fill=tk.BOTH)

        name = tk.Entry(top)
        name.pack(fill=tk.BOTH)

        def save():
            """
            Function for the add button
            """
            # recipient name
            x = name.get().rstrip().replace(" ", "")

            # makes sure there is no duplicates in the treeview
            if x in self.body._messages:
                top.destroy()
            else:
                # insert into treeview
                self.body.insert(x)
                # saves this new contact into DSU file
                saved = SaveData()
                saved.save_into_dsu(self._current_profile.username, "", x, self._current_profile.password,
                                    self._current_profile.dsuserver, self._profile_filename)
                top.destroy()

        # add button that's on the popup page
        but = tk.Button(master=top, text="Add", width=5)
        but.configure(command=save)
        but.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=5)



    def night_on(self):
        """
        Method that turns the text widgets dark and texts green
        adapted by youtube codemy.com
        """
        maincolor = "#000000"
        secondcolor = '#373737'
        textcolor = 'green'

        self.root.config(bg=maincolor)
        self.footer.root.config(bg=maincolor)

        self.body.entry_editor.config(bg=secondcolor, fg=textcolor)
        self.body.send_stuff.config(bg=secondcolor, fg=textcolor)

        self.footer.config(bg=maincolor)


    def night_off(self):
        """
        Method that turns the text widget white and the text black
        adapted by youtube codemy.com
        """

        maincolor = "SystemButtonFace"
        secondcolor = 'SystemButtonFace'
        textcolor = 'black'

        self.root.config(bg=maincolor)
        self.footer.root.config(bg=maincolor)

        self.body.entry_editor.config(bg=secondcolor, fg=textcolor)
        self.body.send_stuff.config(bg=secondcolor, fg=textcolor)

        self.footer.config(bg=maincolor)



    def exit_func(self):
        """
        Method for closing the threading when we click x button on the window adapted from stackoverflow
        """
        self.root.destroy()
        self.control.stop()


    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)

        # new menu item for night mode
        menu_file2 = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file2, label='Night Mode')
        menu_file2.add_command(label='Night Mode On', command=self.night_on)
        menu_file2.add_command(label='Night Mode off', command=self.night_off)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.footer = Footer(self.root, send_callback=self.save_profile, add_callback=self.add)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
        # stops threading even when clicking x button
        # line 577 adapted from stackoverflow
        self.root.protocol('WM_DELETE_WINDOW', self.exit_func)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Messenger App")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x700")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
