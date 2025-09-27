import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
SMTP_HOST = os.getenv('SMTP_HOST') or 'smtp.gmail.com'
SMTP_PORT = int(os.getenv('SMTP_PORT') or 587)
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')

to_email = SMTP_USER
subject = 'VUAVIA - Test email from local test_send_email.py'
body = 'This is a test email to verify SMTP credentials and delivery.'

print('SMTP_HOST=', SMTP_HOST)
print('SMTP_PORT=', SMTP_PORT)
print('SMTP_USER=', SMTP_USER)

msg = MIMEText(body, 'plain', 'utf-8')
msg['From'] = SMTP_USER
msg['To'] = to_email
msg['Subject'] = subject

try:
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(SMTP_USER, [to_email], msg.as_string())
    server.quit()
    print('Email sent successfully')
except Exception as e:
    print('Failed to send email:', repr(e))
    raise
