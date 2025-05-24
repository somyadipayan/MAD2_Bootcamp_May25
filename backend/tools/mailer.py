from flask_mail import Message, Mail
from flask import current_app as app

mail = Mail()

def init_app(app):
    mail.init_app(app)

def send_email(to, subject, body=None, html=None):

    sender = 'noreply@library.com'

    print(subject)

    msg = Message(subject=subject, sender=sender, recipients=[to])
    if body:
        msg.body = body
    if html:
        msg.html = html

    with app.app_context():
        mail.send(msg)