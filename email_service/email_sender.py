import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
import sys
import logging as log 
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import utils

load_dotenv()


log.basicConfig(level=log.INFO,format='%(levelname)s:%(message)s')

GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
FROM_EMAIL = 'shazam0190@gmail.com'

if GMAIL_PASSWORD is None:
    log.error(f'Email Password Missing.... {GMAIL_PASSWORD}')
    sys.exit()

@utils.exception_handler
def send_mail(email_msg_obj,recipient_email):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(FROM_EMAIL, GMAIL_PASSWORD)
        smtp.sendmail(FROM_EMAIL, recipient_email,email_msg_obj.as_string())

@utils.exception_handler
def email_template_obj(table_data,recipient_email): 

    with open('./email_service/index.html', mode='r', encoding='utf-8') as file:
        template_content = file.read()
    
    html_content = Template(template_content).substitute(table_data=table_data)

    #MIME object 
    message = MIMEMultipart()
    message['From'] = FROM_EMAIL
    message['To'] = recipient_email
    message['Subject'] = 'Python Article'
    message.attach(MIMEText(html_content,'html'))
    send_mail(message,recipient_email)
    log.info(f"Email sent to recipient : {recipient_email}")
