import smtplib
import json
from email.message import EmailMessage


def send_newsletter(recipent, con_path="src\\auth\\newsletter\\CONFIG.json"):

    f = open(con_path, "r")
    data = json.load(f)

    gmail_user = data["user"]
    gmail_pass = data["pass"]

    msg = EmailMessage()
    msg.set_content(
        "Gratulacje uzytkowniku, pomyslnie zarejestrowales sie na naszej stronie. Twoje dane zostaly pomyslnie sprzedane!"
    )

    msg["Subject"] = "Potwierdzenie rejestracji w TrendSpire"
    msg["From"] = gmail_user
    msg["To"] = recipent

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(gmail_user, gmail_pass)

    server.send_message(msg)
    server.close()

    print("Email sent!")
