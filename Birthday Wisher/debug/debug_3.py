import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

HOST = "smtp.gmail.com"
# me == my email address
# you == recipient's email address
email_from = "mateusz.hyla.ff@gmail.com"
email_to = "mateusz.hyla.it@gmail.com"
app_pass = "<app_pass>"
img_path = "../assets/images/urodziny-600x400.jpg"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = email_from
msg['To'] = email_to

with open(img_path, 'rb') as f:
    img_data = f.read()

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.<br>
       <img src='https://placehold.co/600x400' alt='Image placeholder' />
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')
image = MIMEImage(img_data, name="Happy Birthday!")
# image = MIMEImage(img_data)


# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)
msg.attach(image)

# Send the message via local SMTP server.
# s = smtplib.SMTP('localhost')
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
# s.sendmail(me, you, msg.as_string())
# s.quit()
try:
    with smtplib.SMTP(HOST, port=587) as conn:
        conn.starttls()
        conn.login(user=email_from, password=app_pass)
        conn.sendmail(from_addr=email_from,
                      to_addrs=email_to,
                      msg=msg.as_string())
except:
    print("Error.")
else:
    print("Email send.")
