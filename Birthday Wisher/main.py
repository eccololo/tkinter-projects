# TODO:
#    1. Zrobić GUI:
#    1.1 Dodać Input dla email_to
#    1.2 Dodać Input dla password
#    1.3 Dodać przycisk send
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

BIRTHDAY_FILE = "./birthdays.csv"
LETTERS_DIR = "./assets/letter_templates"
HOST = "smtp.gmail.com"
APP_PASS = ""
EMAIL_FROM = "mateusz.hyla.ff@gmail.com"
WINDOW_WIDTH = 1120
WINDOW_HEIGHT = 550
CANVAS_BG_COLOR = "#ff6600"


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


def send_birthday_wishes_to_all(recipients_data, host):
    """This function sends email birthday wishes to all recipients."""

    for idx, recipient in enumerate(recipients_data):
        idx += 1
        email_to = recipient[1]
        name_to = recipient[0]
        year_to = recipient[2]
        recipient_age = dt.datetime.now().year - year_to

        message = get_letter_content(LETTERS_DIR).replace("[NAME]", name_to)
        subject = f"Happy birthday! It has been {recipient_age} :-)"

        with smtplib.SMTP(host) as conn:
            conn.starttls()
            conn.login(user=EMAIL_FROM, password=APP_PASS)
            try:
                conn.sendmail(from_addr=EMAIL_FROM,
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


# =============== GUI ==========================
root = Tk()
root.title("Flash Cards App")
center_the_project_window(root)
root.config(pady=40, padx=40)
root.configure(bg='#ff6600')

# Logo
canvas = Canvas(root, width=345, height=455, bg=CANVAS_BG_COLOR, highlightthickness=0)
bw_logo = PhotoImage(file="./assets/images/test_1.png")
canvas.create_image(175, 235, image=bw_logo)
canvas.grid(column=0, row=0)

# Vertical Line 1

# =============== MAIN ==========================
# recipients_data = get_birthday_data(BIRTHDAY_FILE)
# send_birthday_wishes_to_all(recipients_data, HOST)


root.mainloop()
