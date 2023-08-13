import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

s = smtplib.SMTP(host="smtp.gmail.com", port=587)
s.starttls()
s.login("chiarulli14@gmail.com", "dajfosbvggcdemwu")

newPassword = Template("Nuova password: $password")
password_value = "7345"
body = newPassword.substitute(password=password_value)

email = "chiarulli14@gmail.com"
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = email
msg['Subject'] = "This is TEST"
msg.attach(MIMEText(body, 'plain'))

s.send_message(msg)
s.quit()
del msg