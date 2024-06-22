import requests

while True:
    kod = input("Lütfen sorgulamak istediğiniz kodu girin (Çıkmak için 'q' yazın): ")

    if kod.lower() == 'q':
        break

    url = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={kod}&datatype=checkAddress"

    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP hatalarını kontrol et

        data = response.json()

        if "success" in data and data["success"]:
            # Adres bilgilerini daha okunaklı bir şekilde yazdır
            print("Adres Bilgileri:")
            print("-" * 20)
            print("Sokak:", data.get("sokak", "Bilinmiyor"))
            print("Mahalle:", data.get("mahalle", "Bilinmiyor"))
            print("İlçe:", data.get("ilce", "Bilinmiyor"))
            print("İl:", data.get("il", "Bilinmiyor"))
            print("-" * 20)
        else:
            print("Geçersiz kod veya adres bulunamadı.")

    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
