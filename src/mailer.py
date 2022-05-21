import os
import smtplib
from email.mime.text import MIMEText

class Mailer:

  def send(self, mail_to, mail_from, subject, message):
    msg = MIMEText(message, "plain")
    msg["To"] = mail_to
    msg["From"] = mail_from
    msg["Subject"] = subject

    server = smtplib.SMTP(os.environ['SMTP_HOST'], os.environ['SMTP_PORT'])
    server.starttls()
    server.login(os.environ['SMTP_ACCOUNT'], os.environ['SMTP_PASSWORD'])
    server.send_message(msg)
    server.quit()