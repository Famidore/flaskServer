import smtplib
import json


def send_newsletter(recipent, con_path="src\\auth\\newsletter\\CONFIG.json"):

    f = open(con_path, "r")
    data = json.load(f)

    gmail_user = data["user"]
    gmail_pass = data["pass"]

    email_text = "gratulacje uzytkowniku, wygrales iphone"

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(gmail_user, gmail_pass)

    server.sendmail(gmail_user, recipent, email_text)
    server.close()

    print("Email sent!")
