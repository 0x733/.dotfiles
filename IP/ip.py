import requests
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class IPInfo:
    query: str
    continent: str
    continentCode: str
    country: str
    countryCode: str
    region: str
    regionName: str
    city: str
    district: str
    zip: str
    lat: float
    lon: float
    timezone: str
    offset: int
    currency: str
    isp: str
    org: str
    as_: str
    asname: str
    reverse: str
    mobile: bool
    proxy: bool
    hosting: bool

def get_ip_info(ip_address: str) -> Optional[Dict]:
    fields = [
        'status', 'message', 'continent', 'continentCode', 'country',
        'countryCode', 'region', 'regionName', 'city', 'district',
        'zip', 'lat', 'lon', 'timezone', 'offset', 'currency',
        'isp', 'org', 'as', 'asname', 'reverse', 'mobile', 'proxy',
        'hosting', 'query'
    ]
    
    url = f"http://ip-api.com/json/{ip_address}?fields={','.join(fields)}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Bağlantı hatası: {e}")
        return None

def display_ip_info(data: Dict) -> None:
    if data['status'] != 'success':
        print(f"Hata: {data.get('message', 'Bilinmeyen hata')}")
        return

    info = IPInfo(**{k: data.get(k, 'Bilinmiyor') for k in IPInfo.__annotations__})
    
    print("\nIP Adresi Bilgileri:")
    print(f"Sorgulanan IP: {info.query}")
    print(f"Kıta: {info.continent}")
    print(f"Kıta Kodu: {info.continentCode}")
    print(f"Ülke: {info.country}")
    print(f"Ülke Kodu: {info.countryCode}")
    print(f"Bölge Kodu: {info.region}")
    print(f"Bölge Adı: {info.regionName}")
    print(f"Şehir: {info.city}")
    print(f"İlçe: {info.district}")
    print(f"Posta Kodu: {info.zip}")
    print(f"Enlem: {info.lat}")
    print(f"Boylam: {info.lon}")
    print(f"Zaman Dilimi: {info.timezone}")
    print(f"Zaman Dilimi Uzaklığı (Saniye): {info.offset}")
    print(f"Para Birimi: {info.currency}")
    print(f"İSS: {info.isp}")
    print(f"Organizasyon: {info.org}")
    print(f"AS: {info.as_}")
    print(f"AS İsmi: {info.asname}")
    print(f"Ters DNS: {info.reverse}")
    print(f"Mobil Bağlantı: {'Evet' if info.mobile else 'Hayır'}")
    print(f"Proxy Kullanımı: {'Evet' if info.proxy else 'Hayır'}")
    print(f"Hosting Hizmeti: {'Evet' if info.hosting else 'Hayır'}")

def main():
    try:
        ip_address = input("Sorgulamak istediğiniz IP adresini girin: ").strip()
        if not ip_address:
            print("IP adresi boş olamaz.")
            return
            
        if data := get_ip_info(ip_address):
            display_ip_info(data)
            
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    main()