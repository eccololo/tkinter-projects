# TODO:
#    1. Dodać sprawdzenie czy jak dodajemy nowego recipienta to czy nie ma go już w DB.
#       Jesli jest to go nie dodajemy.
#    2. Zobaczyć jak dodać tooltips do checkboxa np.
#    3. Dodać efekty dźwiękowe do przycisków.
#    4. Dodać możliwość wysyłania emaili w postaci HTML.

import datetime as dt
import random
import smtplib
import pandas as pd
import os
import re
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from playsound import playsound
from functools import partial

BIRTHDAY_FILE = "./birthdays.csv"
LETTERS_DIR = "./assets/letter_templates"
HOST = "smtp.gmail.com"
WINDOW_WIDTH = 840
WINDOW_HEIGHT = 550
FILLER_BG_COLOR = "#ff6600"


# =============== FUNCTIONS ==========================
def get_letter_content(letters_dir_path):
    """This function returns a random letter content from a list of letters."""

    letters_no = len(os.listdir(letters_dir_path))
    letter_no = random.randrange(1, letters_no)
    file_name = f"letter_{letter_no}.txt"
    file_path = os.path.join(letters_dir_path, file_name)

    with open(file_path, "r") as f:
        data = f.read()

    return data


def get_birthday_data(file_path):
    """This function returns True if there is someones birthday."""
    day = dt.datetime.now().day
    month = dt.datetime.now().month
    recipients_data = []

    try:
        with open(file_path, 'r') as csvfile:
            df = pd.read_csv(csvfile)
    except FileNotFoundError as err_msg:
        print("Could not read DB csv file. File not found.")
        print(f"Error message: {err_msg}")
    else:
        for index, row in df.iterrows():
            df_day = row['day']
            df_month = row['month']
            df_name = row['name']
            df_year = row['year']
            df_email = row['email']

            if day == df_day and month == df_month:
                recipients_data.append((df_name, df_email, df_year))
    finally:
        return recipients_data


def send_birthday_wishes_to_all(recipients_data):
    """This function sends email birthday wishes to all recipients."""
    global HOST
    app_pass = app_pass_entry.get()
    email_from = email_from_entry.get()
    send_to_all = checkbutton_var.get()
    email_to = email_to_entry.get()
    if send_to_all:
        send_email(email_to, email_from, app_pass)
        if len(recipients_data) > 0:
            for idx, recipient in enumerate(recipients_data):
                idx += 1
                email_to = recipient[1]
                name_to = recipient[0]
                year_to = recipient[2]
                recipient_age = dt.datetime.now().year - year_to
                print(f"Sending email {idx}...")
                send_email(email_to, email_from, app_pass, name_to, recipient_age, str(idx))
        else:
            print("No recipients who celebrate today birthday.")
            ajax_label_txt.config(text="No recipients who celebrate today birthday.")
    else:
        print(f"Sending email ...")
        send_email(email_to, email_from, app_pass)


def send_email(email_to, email_from, app_pass, name="Friend", year="long time", idx=""):
    """This function sends one email to recipient."""
    message = get_letter_content(LETTERS_DIR).replace("[NAME]", name)
    subject = f"Happy birthday! It has been {year} years :-)!"
    try:
        ajax_label_txt.config(text=f"[{idx}] Working...")
        root.update()
        with smtplib.SMTP(HOST, port=587) as conn:
            conn.starttls()
            conn.login(user=email_from, password=app_pass)
            conn.sendmail(from_addr=email_from,
                          to_addrs=email_to,
                          msg=f"Subject:{subject}\n\n"
                              f"{message}.")
    except smtplib.SMTPConnectError as err_msg:
        print(f"Email not sent. Something went wrong with sending email.")
        print(f"Error message: {err_msg}")
        print("-" * 7)
        ajax_label_txt.config(text=f"[{idx}] Failed ...")
    else:
        print(f"Email sent successfuly.")
        ajax_label_txt.config(text=f"[{idx}] Success ...")

    finally:
        email_to_entry.delete(0, END)
        email_from_entry.delete(0, END)
        app_pass_entry.delete(0, END)


def center_the_project_window(w_root):
    """This function centers app window of the center of the screen when it is open. Code taken from
    StackOver Flow."""
    w = WINDOW_WIDTH  # width for the Tk root
    h = WINDOW_HEIGHT  # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    w_root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def get_recipient_data_from_db_as_list():
    """This file reads data from DB file and returns it as a list."""
    output = []
    df = pd.read_csv(BIRTHDAY_FILE)
    for index, row in df.iterrows():
        df_day = row['day']
        df_month = row['month']
        df_name = row['name']
        df_year = row['year']
        df_email = row['email']

        output.append({
            "name": df_name,
            "email": df_email,
            "year": df_year,
            "month": df_month,
            "day": df_day
        })

    return output


def add_recipient_to_db():
    """This function adds recipient data do DB file."""
    email_to = email_add_to_entry.get()
    name_to = email_name_entry.get().capitalize()
    dob = app_dob_entry.get().split("/")
    dob_cleared = clear_dob_entry_data(dob)
    day = dob_cleared[0]
    month = dob_cleared[1]
    year = dob_cleared[2]
    acceptable_year = dt.datetime.now().year - 1

    if not is_email_entry_data_correct(email_to):
        messagebox.showwarning("Wrong Email!", "The email is incorrect.")
        return -1

    if not is_name_entry_data_correct(name_to):
        messagebox.showwarning("Wrong Name!", "The name is incorrect.")
        return -1

    if not day:
        messagebox.showwarning("Wrong Day!", "The day can only be a digit between 1 and 31.")
        return -1

    if not month:
        messagebox.showwarning("Wrong Month!", "The month can only be a digit between 1 and 12.")
        return -1

    if not year:
        messagebox.showwarning("Wrong Year!", f"The year can only be a digit between 1900 and {acceptable_year}.")
        return -1

    db_data = get_recipient_data_from_db_as_list()

    new_recipient = {
        "name": name_to,
        "email": email_to,
        "year": year,
        "month": month,
        "day": day
    }

    db_data.append(new_recipient)
    try:
        df = pd.DataFrame(db_data)
        df.to_csv(BIRTHDAY_FILE, index=False)
    except:
        messagebox.showwarning("Saving Failed!", "Saving recipient data to DB failed."
                                                 "\nContact support at support@gmail.com.")
    else:
        messagebox.showinfo("Saving Success!", f"Data:\nEmail: {email_to}\n"
                                               f"Name: {name_to}\n"
                                               f"DOB: {dob[0]}\\{dob[1]}\\{dob[2]}"
                                               f"\nSaved Successfully!")

        email_add_to_entry.delete(0, END)
        email_name_entry.delete(0, END)
        app_dob_entry.delete(0, END)


def clear_dob_entry_data(data):
    """This function clears dob entry data and return data cleared."""
    day_s = list(data[0])
    day = data[0]
    month_s = list(data[1])
    month = data[1]
    year = data[2]
    acceptable_year = dt.datetime.now().year - 1

    if day_s[0] == "0":
        day = day[1]

    if not day.isdigit():
        day = False

    if month_s[0] == "0":
        month = month[1]

    if not month.isdigit():
        month = False

    if not year.isdigit() or len(year) > 4:
        year = False

    if int(year) < 1900 or int(year) > acceptable_year:
        year = False

    return day, month, year


def is_email_entry_data_correct(email):
    """This function checks if the email is correct. Return False if it is not."""
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$"
    if re.match(regex, email):
        return True
    else:
        return False


def is_name_entry_data_correct(name):
    """This function checks if the name is correct. Return False if it is not."""
    regex = r"^[a-zA-Z][a-zA-Z '-]*$"
    if re.match(regex, name):
        return True
    else:
        return False


def playsound_checked():
    """This function only play sound when checkbox is checked or unchecked."""
    playsound("../assets/sounds/switch.mp3")


# =============== GUI ==========================
root = Tk()
root.title("Flash Cards App by Mateusz Hyla")
center_the_project_window(root)
root.config(pady=40, padx=40)
root.configure(bg='#ff6600')

# Logo
canvas = Canvas(root, width=60, height=60, bg=FILLER_BG_COLOR, highlightthickness=0)
bw_logo = PhotoImage(file="./assets/images/bw_logo_small.png")
canvas.create_image(40, 40, image=bw_logo)
canvas.grid(column=0, row=0, columnspan=6)

# Send
send_label = Label(root, text="SEND", font=("Arial", 24, "bold"), background=FILLER_BG_COLOR)
send_label.grid(row=1, column=2, padx=40, pady=15)

email_to_label = Label(root, text="To:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
email_to_label.grid(row=2, column=1, pady=5)
email_to_entry = Entry(width=35)
email_to_entry.grid(row=2, column=2, padx=10, pady=5, ipady=6)

email_from_label = Label(root, text="From:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
email_from_label.grid(row=3, column=1, pady=5)
email_from_entry = Entry(width=35)
email_from_entry.grid(row=3, column=2, padx=10, pady=5, ipady=6)

app_pass_label = Label(root, text="Pass:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
app_pass_label.grid(row=4, column=1, pady=5)
app_pass_entry = Entry(width=35, show="*")
app_pass_entry.grid(row=4, column=2, padx=10, pady=5, ipady=6)

checkbox_style = Style()
checkbox_style.configure('Action.TCheckbutton', font=("Arial", 11, 'bold'), foreground="#000000",
                         background=FILLER_BG_COLOR, highlightthickness=0)
checkbutton_var = IntVar()
checkbutton = Checkbutton(root, text="To All?", cursor="hand2",
                          style="Action.TCheckbutton", variable=checkbutton_var, command=playsound_checked)
checkbutton.grid(row=5, column=1, padx=10, pady=5, ipady=6)


btn_style = Style()
btn_style.configure('Action.TButton', font=("Arial", 11, 'bold'), foreground="#000000",
                    background="#01d1ff", highlightthickness=0)

recipients_data = get_birthday_data(BIRTHDAY_FILE)
send_birthday_wishes_to_all = partial(send_birthday_wishes_to_all, recipients_data)
send_btn = Button(text="Send", command=send_birthday_wishes_to_all, width=13, style="Action.TButton", cursor="hand2")
send_btn.grid(row=5, column=2, ipady=7, ipadx=7, pady=20)

# Vertical Line 2
liner_2 = Canvas(root, width=50, height=200, bg=FILLER_BG_COLOR, highlightthickness=0)
liner_img_2 = PhotoImage(file="./assets/images/liner.png")
liner_2.create_image(40, 200, image=liner_img_2)
liner_2.grid(row=1, column=3, rowspan=5, padx=(10, 45))


# Add
add_label = Label(root, text="ADD", font=("Arial", 24, "bold"), background=FILLER_BG_COLOR)
add_label.grid(row=1, column=5, padx=40, pady=15)

email_add_to_label = Label(root, text="To:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
email_add_to_label.grid(row=2, column=4, pady=5)
email_add_to_entry = Entry(width=35)
email_add_to_entry.grid(row=2, column=5, padx=10, pady=5, ipady=6)

email_name_label = Label(root, text="Name:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
email_name_label.grid(row=3, column=4, pady=5)
email_name_entry = Entry(width=35)
email_name_entry.grid(row=3, column=5, padx=10, pady=5, ipady=6)

app_dob_label = Label(root, text="DOB:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
app_dob_label.grid(row=4, column=4, pady=5)
app_dob_entry = Entry(width=35)
app_dob_entry.insert(0, "dd/mm/yyyy")
app_dob_entry.grid(row=4, column=5, padx=10, pady=5, ipady=6)

btn_style = Style()
btn_style.configure('Action.TButton', font=("Arial", 11, 'bold'), foreground="#000000",
                    background="#01d1ff", highlightthickness=0)

add_btn = Button(text="Add", command=add_recipient_to_db, width=13, style="Action.TButton", cursor="hand2")
add_btn.grid(row=5, column=5, ipady=7, ipadx=7, pady=20)

ajax_img = PhotoImage(file="./assets/images/work_in_progress.png")
ajax_label = Label(root, image=ajax_img)
ajax_label.grid(column=0, row=7, columnspan=6, padx=0, pady=0)
ajax_label_txt = Label(root, text="", background=FILLER_BG_COLOR, font=("Arial", 10, "bold"))
ajax_label_txt.grid(column=0, row=8, columnspan=6, padx=0, pady=0)

root.mainloop()
