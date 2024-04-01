import smtplib
import json

config_path = "src\\auth\\newsletter\\CONFIG.json"

f = open(config_path, "r")
data = json.load(f)


gmail_user = data["user"]
gmail_pass = data["pass"]

to = "enter mail here"

email_text = "gratulacje uzytkowniku, wygrales iphone"


server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.ehlo()
server.login(gmail_user, gmail_pass)

server.sendmail(gmail_user, to, email_text)
server.close()

print("Email sent!")
