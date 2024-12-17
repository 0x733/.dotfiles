import requests
import json
import sys
from typing import Dict, Optional

def get_address_data(bbk_code: str) -> Optional[Dict]:
    url = f'https://user.goknet.com.tr/sistem/getTTAddressWebservice.php'
    params = {
        'kod': bbk_code,
        'datatype': 'checkAddress'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("İstek zaman aşımına uğradı.")
    except requests.exceptions.RequestException as e:
        print(f"Bağlantı hatası: {e}")
    except json.JSONDecodeError:
        print("Geçersiz yanıt formatı.")
    return None

def parse_flex_list(flex_list: list) -> None:
    for item in flex_list:
        name = item.get('name')
        value = item.get('value')
        if name and value:
            print(f"{name}: {value}")

def display_address_info(data: Dict) -> None:
    for key, value in data.items():
        print(f"\nAdres {key}:")
        
        if flex_list := value.get('flexList', {}).get('flexList'):
            if isinstance(flex_list, list):
                parse_flex_list(flex_list)
        
        if hata_kod := value.get('hataKod'):
            print(f"Hata Kodu: {hata_kod}")
        if hata_mesaj := value.get('hataMesaj'):
            print(f"Hata Mesajı: {hata_mesaj}")

def main():
    try:
        bbk_code = input("BBK kodunu girin: ").strip()
        if not bbk_code:
            print("BBK kodu boş olamaz.")
            return
        
        if data := get_address_data(bbk_code):
            display_address_info(data)
            
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()