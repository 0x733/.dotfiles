import requests
import bs4
import json
from email.message import EmailMessage
import time
from datetime import datetime
import smtplib
import logging

logging.basicConfig(filename='port_check.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bbk = "0000000000"
sender_email = "gonderen@gonderen.com"
app_password = "gmailuygulamasifreniz"
recipient_email = "alici@alici.com"

url = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk}&datatype=checkAddress"

def check_port_status():
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        data = json.loads(str(soup))

        port_value = data['6']['flexList']['flexList'][2]['value']
        error_code = data['6']['hataKod']
        message = data['6']['hataMesaj']

        port_status = 'VAR' if port_value == '1' else 'YOK'

        log_message = f"Port Durumu: {port_status}, Hata Kodu: {error_code}, Mesaj: {message}"
        logging.info(log_message)

        if port_status == 'VAR':
            send_email(message, port_status, error_code)

    except requests.exceptions.RequestException as e:
        logging.error(f"İstek hatası: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"JSON ayrıştırma hatası: {e}")
    except Exception as e:
        logging.error(f"Beklenmeyen hata: {e}")

def send_email(message, port_status, error_code):
    try:
        msg = EmailMessage()
        msg["Subject"] = "TT Port Bilgilendirme"
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg.set_content(f"{message}\nPort durumu: {port_status}\nHata kodu: {error_code}")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
            logging.info("E-posta gönderildi.")
    except smtplib.SMTPException as e:
        logging.error(f"E-posta gönderme hatası: {e}")

while True:
    check_port_status()
    time.sleep(60)