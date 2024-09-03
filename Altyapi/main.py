import requests
import json

def main():
    # Get BBK code from user
    bbk_value = input("BBK kodunu girin: ")
    url = f'https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk_value}&datatype=checkAddress'
    
    try:
        # Send GET request with timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        # Parse JSON data
        data = response.json()
        
        for key, value in data.items():
            print(f"\nAdres {key}:")
            
            flex_list = value.get('flexList', {}).get('flexList')
            if isinstance(flex_list, list):
                for item in flex_list:
                    name = item.get('name')
                    val = item.get('value')
                    if name and val:
                        print(f"{name}: {val}")
                        
            # Check for errors in response
            hata_kod = value.get('hataKod')
            hata_mesaj = value.get('hataMesaj')
            if hata_kod:
                print(f"Hata Kodu: {hata_kod}")
            if hata_mesaj:
                print(f"Hata Mesajı: {hata_mesaj}")
    
    except requests.exceptions.Timeout:
        print("İstek zaman aşımına uğradı.")
    except requests.exceptions.RequestException as e:
        print(f"Bir istek hatası oluştu: {e}")
    except json.JSONDecodeError:
        print("Gelen yanıt geçerli bir JSON formatında değil.")
    except KeyError as e:
        print(f"Beklenmeyen JSON yapısı: {e}")

if __name__ == "__main__":
    main()