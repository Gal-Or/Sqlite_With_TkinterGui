from tkinter import *
from My_Manager import Manager
from tkinter import ttk

# Arrays:
operators = ["=", "!=", ">", "<", ">=", "<=", "IN", "IS NULL", "IS NOT NULL"]

# Global variables:
global mycursor
global table_name
type_dict = {}

manager = Manager.get_instance()  # get a singleton instance
root = Tk()

# Window size and title configuration:
width_val = root.winfo_screenwidth()
height_val = root.winfo_screenheight()
root.geometry("%dx%d" % (width_val, height_val))
root.title("Tables")

# All Frames :
main_frame = Frame(root)
top_frame = Frame(main_frame)
table_frame = Frame(main_frame)
title_list_frame = Frame(main_frame)
listbox_frame = Frame(main_frame)
btns_frame = Frame(main_frame)
query_frame = Frame(main_frame)

# Case Sensitive combobox variable:
var = IntVar()

# Treeview style:
style = ttk.Style()
style.theme_use("clam")  # Pick a theme
style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white")  # configure out tree view  style
style.map('Treeview', background=[('selected', '#ffc0b4')])  # Change selected color
