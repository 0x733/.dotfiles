from seleniumwire import webdriver  # selenium-wire üzerinden tarayıcı trafiğini dinleyeceğiz
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re

# Medya dosyası uzantıları
MEDIA_EXTENSIONS = ['.m3u8', '.mpd', '.mp4', '.mkv']

def is_media_url(url):
    """
    URL'nin bir medya dosyasına ait olup olmadığını kontrol eder.
    """
    return any(url.endswith(ext) for ext in MEDIA_EXTENSIONS)

def find_media_urls(webpage_url):
    """
    Verilen web sayfasını ziyaret eder ve medya dosyası URL'lerini yakalar.
    """
    # Tarayıcı seçenekleri
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcı arka planda çalışsın
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ChromeDriver'ın yolu (sisteminizde doğru yolu belirtin)
    service = Service(executable_path='/usr/bin/chromedriver')

    # Selenium Wire üzerinden ChromeDriver başlat
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Verilen URL'yi aç
    driver.get(webpage_url)

    # Ağ trafiğindeki medya URL'lerini yakala
    media_urls = []
    for request in driver.requests:
        if request.response:
            url = request.url
            if is_media_url(url):
                media_urls.append(url)
    
    driver.quit()  # Tarayıcıyı kapat
    return media_urls

if __name__ == "__main__":
    # Kullanıcıdan URL al
    webpage_url = input("Enter the webpage URL to search for media streams: ").strip()

    # Medya URL'lerini bul
    media_links = find_media_urls(webpage_url)
    
    # Sonuçları ekrana yazdır
    if media_links:
        print("Found media URLs:")
        for link in media_links:
            print(link)
    else:
        print("No media URLs found.")