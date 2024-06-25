import requests
import bs4
import json
import time
from datetime import datetime

bbk = "0000000000"  # buraya goknet.com.tr port sorgu sayfasına adresinizi girince çıkan kodu yapıştırın
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

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        log_message = f"[{current_time}] Port Durumu: {port_status}, Hata Kodu: {error_code}, Mesaj: {message}"
        print(log_message)

    except requests.exceptions.RequestException as e:
        print(f"İstek hatası: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON ayrıştırma hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

while True:
    check_port_status()
    time.sleep(60)