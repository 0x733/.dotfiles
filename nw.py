import requests
import json

while True:  # Kullanıcı doğru bir kod girene kadar devam et
    kod = input("Lütfen sorgulamak istediğiniz kodu girin (Çıkmak için 'q' yazın): ")

    if kod.lower() == 'q':
        break  # Kullanıcı 'q' girerse döngüden çık

    url = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={kod}&datatype=checkAddress"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if "success" in data and data["success"]:  # Başarılı bir sonuç kontrolü
            formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
            print(formatted_data)
        else:
            print("Geçersiz kod veya adres bulunamadı.")

    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
