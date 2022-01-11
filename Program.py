from tkinter import messagebox
import sqlite3
from My_Filter import Filter
from Data import *
import re


def clear_table():
    """
    Deletes the old table.
    """
    for child in table_frame.winfo_children():
        child.destroy()


def clear_btns():
    """
        Deletes the buttons from the frame.
    """
    for child in btns_frame.winfo_children():
        child.destroy()


def clear_title_list():
    """
        Deletes the title of the list.
    """
    for child in title_list_frame.winfo_children():
        child.destroy()


def clear_filters():
    """
        Deletes filter's frame.
    """
    for child in listbox_frame.winfo_children():
        child.destroy()


def clear_query():
    """
        Deletes query's frame.
    """
    for child in query_frame.winfo_children():
        child.destroy()


def create_table(query_str, is_sensitive, clear=False):
    """
    Execute the query, build the table and fill in the data that returns from the db.

    Parameters:
        query_str (string): string of the query to execute.
        is_sensitive (int): 1 if the case sensitive is checked, else 0.
        clear (bool): True if this a new table and we need to clear filters list, default value is False.

    """
    clear_table()
    clear_title_list()
    clear_query()

    if clear:
        clear_filters()

    # create vertical scrollbar
    tree_v_scroll = Scrollbar(table_frame, orient="vertical")
    tree_v_scroll.pack(side=RIGHT, fill=Y)
    # create horizontal scrollbar
    tree_h_scroll = Scrollbar(table_frame, orient="horizontal")
    tree_h_scroll.pack(side=BOTTOM, fill=X)

    # connecting to chinook
    conn = sqlite3.connect('chinook.db')
    global mycursor
    mycursor = conn.cursor()

    if is_sensitive == 0:
        mycursor.execute("PRAGMA case_sensitive_like = off")
    else:
        mycursor.execute("PRAGMA case_sensitive_like = on")
    mycursor.execute(query_str)

    # get all columns names
    columns_names = list(map(lambda xx: xx[0], mycursor.description))

    # create the tree view
    tree = ttk.Treeview(table_frame, columns=columns_names, height=6, show="headings",
                        yscrollcommand=tree_v_scroll.set, xscrollcommand=tree_h_scroll.set,
                        style="mystyle.Treeview")
    tree.tag_configure('oddrow', background='#eaeaea')
    tree.tag_configure('evenrow', background='#fdf3f1')

    tree.pack(side='top')

    # set scrollbars configuration
    tree_v_scroll.config(command=tree.yview)
    tree_h_scroll.config(command=tree.xview)

    # add data to the tree
    for name in columns_names:
        tree.heading(name, text=name, anchor=W)
        tree.column(name)

    for x in tree.get_children():
        tree.delete(x)

    count = 0
    results = mycursor.fetchall()
    for row in results:
        if count % 2 == 0:
            tree.insert('', 'end', values=row[0:len(columns_names)], tags='evenrow')
        else:
            tree.insert('', 'end', values=row[0:len(columns_names)], tags='oddrow')
        count += 1

    s = ttk.Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="#ffc0b4")

    create_title_list_frame()
    if clear:
        create_listbox_frame()

    conn.close()


def create_title_list_frame():
    """
    Creates a new label to title of the filters list.
    """
    title = Label(title_list_frame, text="Chosen Filters:", font=('bold', 12))
    title.pack(side=TOP)


def create_listbox_frame():
    """
    Creates a new listbox to all the filters with a scrollbar.
    """
    # create scrollbar to the listbox
    listbox_scrollbar = Scrollbar(listbox_frame, orient=VERTICAL)

    # create filters list
    filters_list = Listbox(listbox_frame, height=6,
                           width=50,
                           bg="#e5e5e5",
                           activestyle='dotbox',
                           selectbackground="black",
                           yscrollcommand=listbox_scrollbar.set)

    # configure scrollbar
    listbox_scrollbar.config(command=filters_list.yview)

    listbox_scrollbar.pack(side=RIGHT, fill=Y)
    filters_list.pack(side=TOP)

    create_btns_frame(filters_list)


def create_btns_frame(filters_list):
    """
    Creates "Add Filter" button, "Delete Filter" button, "Case Sensitive" checkbox and put them in btns_frame.

    Parameters:
        filters_list(list) - the list of all existing filters.
    """
    # create "add filter" btn
    add_filter_btn = Button(btns_frame, text="Add Filter", width=10, bd='5', command=add_query)
    # create "delete_filter" btn
    delete_filter_btn = Button(btns_frame, text="Delete Filter", width=10, bd='5',
                               command=lambda: delete_filter(filters_list, var))
    # create "case sensitive" checkbox
    # var = IntVar() ---> define outside
    case_sens_check = Checkbutton(btns_frame, text="case sensitive", variable=var)

    add_filter_btn.grid(row=0, column=0, padx=5)
    delete_filter_btn.grid(row=0, column=1, padx=5)
    case_sens_check.grid(row=0, column=2, padx=5)


def delete_filter(filters_list, is_sensitive):
    """
    Executed when "delete_filter_btn" is clicked. Deletes the selected filter from the listbox.

    Parameters:
        filters_list(list) - the list of all existing filters.
        is_sensitive (int): 1 if the case sensitive is checked, else 0.
    """
    x = filters_list.curselection()
    if x:  # checks if the tuple is not empty -> can be empty when click on delete without select item in the list box
        manager.remove(manager.all_filters[filters_list.curselection()[0]])
        filters_list.delete(ANCHOR)
        build_query(is_sensitive)


def build_query(is_sensitive):
    """
    Create string query from all the filters that exists in the filters listbox.
    Parameters:
        is_sensitive(int): 1 if the case sensitive is checked, else 0.
    """
    # connecting to chinook
    global table_name
    query = "SELECT *  FROM " + table_name
    if len(manager.all_filters) > 0:
        query += " WHERE "
    size = len(manager.all_filters)
    i = 0
    for filter in manager.all_filters:
        query += str(filter)
        if i < size - 1:
            query += " AND "
        i += 1
    if is_sensitive == 0:
        query += " COLLATE NOCASE"

    create_table(query, is_sensitive)


def submit_action(attr, op, is_sensitive, val=""):
    """
    Execute when "submit_btn" is clicked. This function add the filter to the filters list and execute
    the "build_query" function.

    Parameters:
        attr(string): The name of the column/attribute in the table from the filter.
        op(string): The operator of the filter.
        is_sensitive(int): 1 if the case sensitive is checked, else 0.
        val(string): The value from the filter.
    """
    # check the input..
    if type_dict[attr] == 'INTEGER' or 'NUMERIC' in type_dict[attr] and val != '' and not val.isnumeric():
        err_msg('Input must be a number!')
        clear_query()
    elif type_dict[attr] == 'DATETIME':
        p = re.compile(r'(0[1-9]|[12]\d|3[01])/(0[1-9]|1[012])/[12][0-9]{3}')

        if p.match(val) is None:
            err_msg('Date Input must be in pattern DD/MM/YYYY')
            clear_query()
        else:
            add_to_listbox(attr, op, val)
            build_query(is_sensitive)

    else:
        add_to_listbox(attr, op, val)
        build_query(is_sensitive)


def err_msg(msg):
    """
    Display the msg in pop up box to the user.

    Parameters:
        msg(string): The message that should display in the pop message.
    """
    messagebox.showerror('Invalid Input', msg)


def add_query():
    """
    Creates "add_query" frame, "combo_attr" combobox and "combo_op" combobox.
    (Creates a new frame to new query).
    """
    clear_query()
    global mycursor
    # get all columns names
    columns_names = list(map(lambda xx: xx[0], mycursor.description))
    combo_attr = create_combobox(query_frame, columns_names, 0, 0)
    combo_attr.bind("<<ComboboxSelected>>", lambda event: callback_combo_attr(event))
    combo_attr.set("choose attribute")


def add_to_listbox(attr, op, val):  # on submit pressed
    """
    Creates a new filter and add to the listbox.

    Parameters:
        attr(string): The name of the column/attribute in the table from the filter.
        op(string): The operator of the filter.
        val(string): The value from the filter.

    """
    new_filter = Filter(attr, op, type_dict[attr], val)
    list_size = len(manager.all_filters)
    manager.add_filter(new_filter)
    if list_size < len(manager.all_filters):
        listbox_frame.winfo_children()[1].insert(END, new_filter.__str__())
    clear_query()


def create_combobox(frame, vals, r, c):
    """
    Creates a new combobox and adding to the frame.

    Parameters:
        frame(Frame): The frame that we want to add the combobox.
        vals(String[]): Array of strings. The options to the combobox.
        r(int): Row number in the frame to place the combobox in.
        c(int): column number in the frame to place the combobox in.

    returns:
    combo(Combobox): New combobox that we created.

    """
    combo = ttk.Combobox(frame, values=vals)
    combo.grid(row=r, column=c, padx=10)
    return combo


def init_dict():
    """
    init a dictionary "type_dict".
    key -> column name.
    value -> data type.
    """
    # connecting to chinook
    conn = sqlite3.connect('chinook.db')
    global mycursor
    mycursor = conn.cursor()

    global table_name
    mycursor.execute("PRAGMA table_info(" + table_name + ")")
    info = mycursor.fetchall()
    print(list(info))
    for col in info:
        type_dict[col[1]] = col[2]

    # print(type_dict.items())
    conn.close()


def callback_combo_attr(event):
    combo_op = create_combobox(query_frame, operators, 0, 1)
    combo_op.set("choose operator")
    combo_op.bind("<<ComboboxSelected>>", lambda event2: callback_choose_op(event2, event.widget.get()))


def callback_choose_table(event):
    """
    Executed when the "combo_tables" is clicked.
    This function creates a new query and execute the function "create_table".
    Parameters:
        event(Event): The event that execute the function.

    """
    type_dict.clear()
    # connecting to chinook
    conn = sqlite3.connect('chinook.db')
    global mycursor
    mycursor = conn.cursor()

    manager.all_filters = []
    global table_name
    clear_filters()
    table_name = event.widget.get()
    # create query string and execute it
    query_str = "SELECT *  FROM " + table_name
    init_dict()
    create_table(query_str, 0, True)


def callback_choose_op(event, attr):
    """
    Executed when the "combo_op" is clicked.
    This function creates or not creates according to the operator that have been chosen ,a new Entry for user input.
    In Addition the function Creates a submit button.

    Parameters:
        event(Event): The event that execute the function.
        attr(string): The name of the column/attribute in the table from the filter.

    """
    all_widgets = query_frame.winfo_children()
    for widget in all_widgets:
        if str(widget.__class__) == "<class 'tkinter.Entry'>" or str(widget.__class__) == "<class 'tkinter.Button'>":
            widget.destroy()

    op_val = event.widget.get()
    if op_val != "IS NULL" and op_val != "IS NOT NULL":
        input_txt = Entry(query_frame)
        input_txt.grid(row=0, column=2, padx=10)
        # create "submit" btn
        submit_btn = Button(query_frame, text="Submit", bd='5',
                            command=lambda: submit_action(attr, op_val, var.get(), input_txt.get()))
    else:
        # create "submit" btn
        submit_btn = Button(query_frame, text="Submit", bd='5',
                            command=lambda: submit_action(attr, op_val, var.get()))

    submit_btn.grid(row=1, column=1, pady=10)
    all_widgets = query_frame.winfo_children()
