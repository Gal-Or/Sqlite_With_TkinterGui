# Name: Gal Or        -> ID : 316083690
# Name: Koral Nataf   -> ID : 208726257
from Program import *


def main():
    root.wm_attributes("-topmost", 1)  # save the window always on top of the screen

    main_frame.pack(fill=BOTH, expand=1)
    top_frame.pack(padx=10, pady=10)

    lbl_title = Label(top_frame, text="Choose Table : ", font=('bold', 12), pady=10, padx=10)
    lbl_title.grid(row=0, column=0)

    conn = sqlite3.connect('chinook.db')
    global mycursor
    mycursor = conn.cursor()
    values = list(conn.execute("SELECT name FROM sqlite_master WHERE type='table';"))

    conn.close()
    combo_tables = create_combobox(top_frame, values, 0, 1)

    table_frame.pack(padx=100, pady=10)
    title_list_frame.pack(padx=100, pady=5)
    listbox_frame.pack(padx=10, pady=10)
    btns_frame.pack(padx=10, pady=10)
    query_frame.pack(padx=10, pady=10)

    combo_tables.bind("<<ComboboxSelected>>", callback_choose_table)

    root.mainloop()


# run main
main()
