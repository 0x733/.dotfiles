import requests
import json
import time
from datetime import datetime, timedelta

bbk = "0000000000"
url = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk}&datatype=checkAddress"
end_time = datetime.now() + timedelta(seconds=10)

def check_port_status():
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        if '6' in json_data and 'flexList' in json_data['6'] and 'flexList' in json_data['6']['flexList'] and len(json_data['6']['flexList']['flexList']) > 2:
            port_value = json_data['6']['flexList']['flexList'][2]['value']
            error_code = json_data['6']['hataKod']
            message = json_data['6']['hataMesaj']

            port_status = 'VAR' if port_value == '1' else 'YOK'

            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")

            log_message = f"[{current_time}] Port Durumu: {port_status}, Hata Kodu: {error_code}, Mesaj: {message}"
            print(log_message)
        else:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Beklenen JSON yapısı bulunamadı")

    except requests.exceptions.RequestException as e:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] İstek hatası: {e}")
    except json.JSONDecodeError as e:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] JSON ayrıştırma hatası: {e}")
    except Exception as e:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Beklenmeyen hata: {e}")

while datetime.now() < end_time:
    check_port_status()
    time.sleep(60)

print("Program sonlandı.")