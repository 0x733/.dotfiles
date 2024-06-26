import requests
import json

# Kullanıcıdan bbk kodunu al
bbk_value = input("BBK kodunu girin: ")
url = f'https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk_value}&datatype=checkAddress'

# GET isteği gönder
response = requests.get(url)

# İstek başarılı mı kontrol et
if response.status_code == 200:
    data = response.json()
    
    for key, value in data.items():
        print(f"\nAdres {key}:")
        if 'flexList' in value and isinstance(value['flexList'], dict) and 'flexList' in value['flexList']:
            flex_list = value['flexList']['flexList']
            if isinstance(flex_list, list):
                for item in flex_list:
                    if isinstance(item, dict) and 'name' in item and 'value' in item:
                        print(f"{item['name']}: {item['value']}")
        if 'hataKod' in value:
            print(f"Hata Kodu: {value['hataKod']}")
        if 'hataMesaj' in value:
            print(f"Hata Mesajı: {value['hataMesaj']}")
else:
    print(f'İstek başarısız oldu. HTTP Durum Kodu: {response.status_code}')

