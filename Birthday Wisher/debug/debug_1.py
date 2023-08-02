import datetime as dt
import smtplib

HOST = "smtp.gmail.com"
email_from = "mateusz.hyla.ff@gmail.com"
app_pass = "<app_pass>"

recipients_data = [["Kaska", "mateusz.hyla.it@gmail.com", 1985, 8, 2],
                   ["Mateusz", "mateusz.hyla.it@gmail.com", 1987, 8, 2]]

for idx, recipient in enumerate(recipients_data):
    idx += 1
    email_to = recipient[1]
    name_to = recipient[0]
    year_to = recipient[2]
    recipient_age = dt.datetime.now().year - year_to

    message = """Dear [NAME],

Happy birthday!

All the best for the year!

Angela"""
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
