import requests

def ip_sorgu(ip_adresi):
    try:
        # Sorgu URL'sini fields parametresi ile özelleştir
        url = f"http://ip-api.com/json/{ip_adresi}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        
        # API'ye istek gönder
        response = requests.get(url)
        
        # Yanıtı kontrol et
        if response.status_code == 200:
            ip_bilgileri = response.json()
            
            # Sorgu durumu başarılı mı kontrol et
            if ip_bilgileri['status'] == 'success':
                # Gelen bilgileri formatla ve yazdır
                print("IP Adresi Bilgileri:")
                print(f"Sorgulanan IP: {ip_bilgileri.get('query', 'Bilinmiyor')}")
                print(f"Kıta: {ip_bilgileri.get('continent', 'Bilinmiyor')}")
                print(f"Kıta Kodu: {ip_bilgileri.get('continentCode', 'Bilinmiyor')}")
                print(f"Ülke: {ip_bilgileri.get('country', 'Bilinmiyor')}")
                print(f"Ülke Kodu: {ip_bilgileri.get('countryCode', 'Bilinmiyor')}")
                print(f"Bölge Kodu: {ip_bilgileri.get('region', 'Bilinmiyor')}")
                print(f"Bölge Adı: {ip_bilgileri.get('regionName', 'Bilinmiyor')}")
                print(f"Şehir: {ip_bilgileri.get('city', 'Bilinmiyor')}")
                print(f"İlçe: {ip_bilgileri.get('district', 'Bilinmiyor')}")
                print(f"Posta Kodu: {ip_bilgileri.get('zip', 'Bilinmiyor')}")
                print(f"Enlem: {ip_bilgileri.get('lat', 'Bilinmiyor')}")
                print(f"Boylam: {ip_bilgileri.get('lon', 'Bilinmiyor')}")
                print(f"Zaman Dilimi: {ip_bilgileri.get('timezone', 'Bilinmiyor')}")
                print(f"Zaman Dilimi Uzaklığı (Saniye): {ip_bilgileri.get('offset', 'Bilinmiyor')}")
                print(f"Para Birimi: {ip_bilgileri.get('currency', 'Bilinmiyor')}")
                print(f"İSS (İnternet Servis Sağlayıcısı): {ip_bilgileri.get('isp', 'Bilinmiyor')}")
                print(f"Organizasyon: {ip_bilgileri.get('org', 'Bilinmiyor')}")
                print(f"AS: {ip_bilgileri.get('as', 'Bilinmiyor')}")
                print(f"AS İsmi: {ip_bilgileri.get('asname', 'Bilinmiyor')}")
                print(f"Ters DNS: {ip_bilgileri.get('reverse', 'Bilinmiyor')}")
                print(f"Mobil Bağlantı: {'Evet' if ip_bilgileri.get('mobile') else 'Hayır'}")
                print(f"Proxy Kullanımı: {'Evet' if ip_bilgileri.get('proxy') else 'Hayır'}")
                print(f"Hosting Hizmeti: {'Evet' if ip_bilgileri.get('hosting') else 'Hayır'}")
            else:
                print(f"Hata: {ip_bilgileri.get('message', 'Bilinmeyen hata')}")
        else:
            print(f"IP adresi sorgulanamadı. Hata Kodu: {response.status_code}")
    except Exception as e:
        print(f"Hata: {e}")

# IP adresini buradan girebilirsiniz
ip_adresi = input("Sorgulamak istediğiniz IP adresini girin: ")
ip_sorgu(ip_adresi)
