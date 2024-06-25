import requests
import json
import time
from datetime import datetime, timedelta
from json2html import json2html

bbk = "0000000000"
url = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk}&datatype=checkAddress"
end_time = datetime.now() + timedelta(seconds=10)

def check_port_status():
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        port_value = json_data.get('6', {}).get('flexList', {}).get('flexList', [])[2].get('value', '')
        error_code = json_data.get('6', {}).get('hataKod', '')
        message = json_data.get('6', {}).get('hataMesaj', '')

        port_status = 'VAR' if port_value == '1' else 'YOK'

        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")

        log_message = f"[{current_time}] Port Durumu: {port_status}, Hata Kodu: {error_code}, Mesaj: {message}"
        print(log_message)

        # JSON verisini HTML'e dönüştür
        html_table = json2html.convert(json=json_data)

        # HTML tablosunu dosyaya yaz
        filename = f"port_status_{current_time}.html"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_table)
            print(f"HTML dosyası kaydedildi: {filename}")

    except requests.exceptions.RequestException as e:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        print(f"[{current_time}] İstek hatası: {e}")
    except json.JSONDecodeError as e:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        print(f"[{current_time}] JSON ayrıştırma hatası: {e}")
    except Exception as e:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        print(f"[{current_time}] Beklenmeyen hata: {e}")

while datetime.now() < end_time:
    check_port_status()
    time.sleep(60)

print("Program sonlandı.")