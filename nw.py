import requests
import json
import csv

# Kullanıcıdan kod al
kod = input("Lütfen kodunuzu girin: ")

# API isteği gönder
url = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={kod}&datatype=checkAddress"
response = requests.get(url)

# Hata kontrolü: İstek başarısız olursa
if response.status_code != 200:
    print(f"Hata: API isteği başarısız oldu. Hata kodu: {response.status_code}")
    exit(1)

# JSON verilerini ayrıştır
data = response.json()

# CSV dosyası oluştur
with open("adresler.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    # Başlıkları yaz
    writer.writerow(["Anahtar", "Parametre", "Değer"])

    # Verileri CSV'ye yaz
    for key, value in data.items():
        for item in value["flexList"]["flexList"]:
            # Boş değerleri ve hata bilgilerini atla
            if not item["value"] or item["name"] in ["hataKod", "hataMesaj"]:
                continue

            writer.writerow([key, item["name"], item["value"]])

print("Adres bilgileri 'adresler.csv' dosyasına kaydedildi.")
