import requests
import bs4
import json
import time
import logging
from datetime import datetime

logging.basicConfig(filename='port_check.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

with open('config.json') as config_file:
    config = json.load(config_file)

bbk = config["bbk"]
check_interval = config["check_interval"]
max_retries = config["max_retries"]
retry_delay = config["retry_delay"]

url = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk}&datatype=checkAddress"

def check_port_status():
    for attempt in range(max_retries):
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

            break

        except requests.exceptions.RequestException as e:
            logging.error(f"İstek hatası (Deneme {attempt + 1}/{max_retries}): {e}")
        except json.JSONDecodeError as e:
            logging.error(f"JSON ayrıştırma hatası (Deneme {attempt + 1}/{max_retries}): {e}")
        except Exception as e:
            logging.error(f"Beklenmeyen hata (Deneme {attempt + 1}/{max_retries}): {e}")

        if attempt < max_retries - 1:
            time.sleep(retry_delay)

while True:
    check_port_status()
    time.sleep(check_interval)