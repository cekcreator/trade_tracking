import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email():
    most_recent_trade = pd.read_excel('./csvs/trades.xlsx', engine="openpyxl")
    most_recent_trade = most_recent_trade.iloc[-1]

    email_code = os.getenv('email_code')
    email_sender = os.getenv('email_sender')
    email_receiver = os.getenv('email_receiver')

    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = 'Nancy Pelosi Trades'
    body = (f"Stock {most_recent_trade['Stock']}, \n"
            f"Amount {most_recent_trade['Amount']}, \n "
            f"Traded {most_recent_trade['Traded']}, \n"
            f"Disclosed {most_recent_trade['Disclosed']}, \n"
            f"Description {most_recent_trade['Description']}, \n"
            f"Date retrieved {most_recent_trade['Date_Retrieved']}")
    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_sender, email_code)
    server.sendmail(email_sender, email_receiver, message.as_string())
    server.quit()


if __name__ == '__main__':
    send_email()
    print('Added to csv file')
