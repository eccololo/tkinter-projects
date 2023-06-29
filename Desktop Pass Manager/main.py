from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from playsound import playsound
from random import randint, shuffle, choice
import pyperclip
import re


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    """This function generate strong password."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 11))]
    password_list += [choice(symbols) for _ in range(randint(3, 4))]
    password_list += [choice(numbers) for _ in range(randint(3, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    entry_pass.insert(0, password)

    pyperclip.copy(password)

    label_copied.config(text="Copied!")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_pass():
    """This function saves enetred data by user to DB like www, login and password."""
    www = entry_www.get()
    login = entry_login.get()
    password = entry_pass.get()

    duplicate_proceed = False
    is_duplicates = check_for_duplicates(www=www, login=login)

    if is_duplicates:
        duplicate_proceed = messagebox.askyesno(title="Duplicated Detected!",
                                                message="This website address and login are already in database. Do you want to update your pass?")

    if is_duplicates:
        override_pass(www=www, login=login, password=password)
        messagebox.showinfo(title="Success!", message="Password updated!")
        clear_entries_labels()

    elif not duplicate_proceed:
        is_data_ok = validate_data(www=www, login=login, password=password)

        if is_data_ok:

            is_ok = messagebox.askokcancel(title=www, message=f"Details:\nlogin: {login}\npassword: {password}\n"
                                                              f"Is it ok to save?")

            if is_ok:
                with open(DB_PASS_FILE_PATH, "a") as f:
                    f.write(f"{www} | {login} | {password}\n")

                clear_entries_labels()
                playsound("./ping.mp3")


DB_PASS_FILE_PATH = "./pass-data.txt"

root = Tk()
root.title("Desktop Pass Manager")
root.geometry("520x400")
root.config(pady=50, padx=50)

canvas = Canvas(root, width=200, height=200)
logo_image = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

label_www = Label(root, text="Website: ")
label_www.grid(row=1, column=0)

label_login = Label(root, text="Email / Username: ")
label_login.grid(row=2, column=0)

label_pass = Label(root, text="Password: ")
label_pass.grid(row=3, column=0)

label_copied = Label(root, text="")
label_copied.grid(row=3, column=3)

entry_www = Entry(root, width=48)
entry_www.focus()
entry_www.grid(row=1, column=1, columnspan=2)

entry_login = Entry(root, width=48)
entry_login.insert(0, "mateusz@gmail.com")
entry_login.grid(row=2, column=1, columnspan=2)

entry_pass = Entry(root, width=34)
entry_pass.grid(row=3, column=1)

btn_pass = Button(root, text="Generate Pass", command=gen_pass)
btn_pass.grid(row=3, column=2)

btn_add = Button(root, text="Add", command=add_pass, width=48)
btn_add.grid(row=4, column=1, columnspan=2)

root.mainloop()
