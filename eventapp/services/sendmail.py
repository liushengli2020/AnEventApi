import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from eventapp.models import EmailSender,User
import base64

def sendmail(sender, password, receiver, smtp, port, subject, plain_text, html=None):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    if plain_text:
        message.attach(MIMEText(plain_text, "plain"))
    if html:
        message.attach(MIMEText(plain_text, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())


def send_notif_mail(event_id, user_id, isQuit):
    sender = EmailSender.query.first()
    subject = isQuit and 'event quit' or 'event signed up'
    body = isQuit and f'{user_id} quit event {event_id}' or f'{user_id} sign up event {event_id}'
    password = base64.b64decode(sender.password).decode('utf8')
    sendmail(sender.sender_email, password, sender.sender_email, sender.smtp_server, sender.port, subject, body )