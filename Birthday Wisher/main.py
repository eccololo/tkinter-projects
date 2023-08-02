# TODO:
#    1. Zrobić GUI:
#    1.4 Dodać Input dla imienia do dodania do DB
#    1.5 Dodać Input dla emailu_to do dodania do DB
#    1.6 Dodać Input dla daty urodzenia do dodania dla DB
#    1.6.1 Dodac przycisk add dodajacy dane do DB.
#    1.7 Dodać canvas i logo na środku canvas.
#    1.8 Dodac image Ajax kiedy wysyłamy email.

import datetime as dt
import random
import smtplib
import pandas as pd
import os
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from playsound import playsound
from functools import partial

BIRTHDAY_FILE = "./birthdays.csv"
LETTERS_DIR = "./assets/letter_templates"
HOST = "smtp.gmail.com"
WINDOW_WIDTH = 1120
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
        return f.read()


def get_birthday_data(file_path):
    """This function returns True if there is someones birthday."""
    day = dt.datetime.now().day
    month = dt.datetime.now().month
    recipients_data = []

    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        df_day = row['day']
        df_month = row['month']
        df_name = row['name']
        df_year = row['year']
        df_email = row['email']

        if day == df_day and month == df_month:
            recipients_data.append((df_name, df_email, df_year))

    return recipients_data


def send_birthday_wishes_to_all(recipients_data):
    """This function sends email birthday wishes to all recipients."""

    global HOST
    app_pass = app_pass_entry.get()
    email_from = email_from_entry.get()
    # FIXME:
    #    1. Zrobic tak aby use mogl tez podac email i do niego tez wysle sie emaila.
    email_to_add = email_to_entry.get()
    for idx, recipient in enumerate(recipients_data):
        idx += 1
        email_to = recipient[1]
        name_to = recipient[0]
        year_to = recipient[2]
        recipient_age = dt.datetime.now().year - year_to

        message = get_letter_content(LETTERS_DIR).replace("[NAME]", name_to)
        subject = f"Happy birthday! It has been {recipient_age} :-)"

        with smtplib.SMTP(HOST) as conn:
            conn.starttls()
            conn.login(user=email_from, password=app_pass)
            try:
                conn.sendmail(from_addr=email_from,
                              to_addrs=email_to,
                              msg=f"Subject:{subject}\n\n"
                                  f"{message}.")
            except:
                print(f"Email not sent. Something went wrong with email no_{idx}.")
            else:
                print(f"[{idx}]Email sent successfuly.")


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
    name_to = email_name_entry.get()
    dob = app_dob_entry.get().split("/")
    dob_cleared = clear_dob_entry_data(dob)
    day = dob_cleared[0]
    month = dob_cleared[1]
    year = dob_cleared[2]
    acceptable_year = dt.datetime.now().year - 1

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


# =============== GUI ==========================
root = Tk()
root.title("Flash Cards App")
center_the_project_window(root)
root.config(pady=40, padx=40)
root.configure(bg='#ff6600')

# # Logo
# canvas = Canvas(root, width=305, height=455, bg=FILLER_BG_COLOR, highlightthickness=0)
# bw_logo = PhotoImage(file="./assets/images/test_1.png")
# canvas.create_image(145, 235, image=bw_logo)
# canvas.grid(column=0, row=0, rowspan=5)
#
# # Vertical Line 1
# liner_1 = Canvas(root, width=50, height=200, bg=FILLER_BG_COLOR, highlightthickness=0)
# liner_img_1 = PhotoImage(file="./assets/images/liner.png")
# liner_1.create_image(40, 200, image=liner_img_1)
# liner_1.grid(column=1, row=0, rowspan=5)

# Send
send_label = Label(root, text="SEND", font=("Arial", 24, "bold"), background=FILLER_BG_COLOR)
send_label.grid(row=0, column=1, padx=40, pady=15)

email_to_label = Label(root, text="To:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
email_to_label.grid(row=1, column=0, pady=5)
email_to_entry = Entry(width=35)
email_to_entry.grid(row=1, column=1, padx=10, pady=5, ipady=6)

email_from_label = Label(root, text="From:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
email_from_label.grid(row=2, column=0, pady=5)
email_from_entry = Entry(width=35)
email_from_entry.grid(row=2, column=1, padx=10, pady=5, ipady=6)

app_pass_label = Label(root, text="Pass:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
app_pass_label.grid(row=3, column=0, pady=5)
app_pass_entry = Entry(width=35, show="*")
app_pass_entry.grid(row=3, column=1, padx=10, pady=5, ipady=6)

btn_style = Style()
btn_style.configure('Action.TButton', font=("Arial", 11, 'bold'), foreground="#000000",
                    background="#01d1ff", highlightthickness=0)

recipients_data = get_birthday_data(BIRTHDAY_FILE)
send_birthday_wishes_to_all = partial(send_birthday_wishes_to_all, recipients_data)
send_btn = Button(text="Send", command=send_birthday_wishes_to_all, width=13, style="Action.TButton")
send_btn.grid(row=4, column=1, ipady=7, ipadx=7, pady=20)

# Vertical Line 1
liner_1 = Canvas(root, width=50, height=200, bg=FILLER_BG_COLOR, highlightthickness=0)
liner_img_1 = PhotoImage(file="./assets/images/liner.png")
liner_1.create_image(40, 200, image=liner_img_1)
liner_1.grid(row=0, column=2, rowspan=5, padx=(10, 45))

# Add
add_label = Label(root, text="Add", font=("Arial", 24, "bold"), background=FILLER_BG_COLOR)
add_label.grid(row=0, column=4, padx=40, pady=15)

email_add_to_label = Label(root, text="To:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
email_add_to_label.grid(row=1, column=3, pady=5)
email_add_to_entry = Entry(width=35)
email_add_to_entry.grid(row=1, column=4, padx=10, pady=5, ipady=6)

email_name_label = Label(root, text="Name:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
email_name_label.grid(row=2, column=3, pady=5)
email_name_entry = Entry(width=35)
email_name_entry.grid(row=2, column=4, padx=10, pady=5, ipady=6)

app_dob_label = Label(root, text="DOB:", font=("Arial", 14, "bold"), background=FILLER_BG_COLOR)
app_dob_label.grid(row=3, column=3, pady=5)
app_dob_entry = Entry(width=35)
app_dob_entry.insert(0, "dd/mm/yyyy")
app_dob_entry.grid(row=3, column=4, padx=10, pady=5, ipady=6)

btn_style = Style()
btn_style.configure('Action.TButton', font=("Arial", 11, 'bold'), foreground="#000000",
                    background="#01d1ff", highlightthickness=0)

add_btn = Button(text="Add", command=add_recipient_to_db, width=13, style="Action.TButton")
add_btn.grid(row=4, column=4, ipady=7, ipadx=7, pady=20)

root.mainloop()
