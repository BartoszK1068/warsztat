from email.message import EmailMessage
import imghdr
import smtplib


PASSWORD = "foeq fgsj rsrv dbpz"
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
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


def send_zgloszenie(imie: str, nazwisko: str, tel: str, termin: str, opis: str, login: str) -> None:
    """
    Wysyła maila z informacją o nowym zgłoszeniu.
    """
    email_message = EmailMessage()
    email_message["Subject"] = f"Nowe zgłoszenie od {imie} {nazwisko}"
    email_message.set_content(
        f"Nowe zgłoszenie:\n"
        f"Imię i nazwisko: {imie} {nazwisko}\n"
        f"Login: {login}\n"
        f"Telefon: {tel}\n"
        f"Termin: {termin}\n"
        f"Opis: {opis}\n"
    )

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
