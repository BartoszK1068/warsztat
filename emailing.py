from email.message import EmailMessage
import imghdr
import smtplib


PASSWORD= "foeq fgsj rsrv dbpz"
SENDER = "bartoszkusinski03@gmail.com" 
RECEIVER = "bartoszkusinski03@gmail.com" 

def send_email():
    print("sent email")


def send_email_1():
    email_message = EmailMessage()
    email_message["Subject"] = "new customer"
    email_message.set_content("hey new customer")



    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER,PASSWORD)
    gmail.sendmail(SENDER,RECEIVER,email_message.as_string())
    gmail.quit()