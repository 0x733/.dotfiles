from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
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
    Verilen web sayfasını ziyaret eder ve DevTools Protocol ile medya dosyası URL'lerini yakalar.
    """
    # Tarayıcı seçenekleri
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcı arka planda çalışsın
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # ChromeDriver'ın yolu (sisteminizde doğru yolu belirtin)
    service = Service(executable_path='/usr/bin/chromedriver')

    # Selenium ile ChromeDriver başlat
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # DevTools Protocol ile tarayıcıya bağlan
    driver.execute_cdp_cmd('Network.enable', {})

    # Yakalanan medya URL'lerini depolamak için liste
    media_urls = []

    def process_event(event):
        """ Her ağ isteği için medya URL'si olup olmadığını kontrol eder. """
        try:
            request_url = event['params']['request']['url']
            if is_media_url(request_url):
                print(f"Found media URL: {request_url}")
                media_urls.append(request_url)
        except KeyError:
            pass

    # Ağ trafiğini dinle
    driver.request_interceptor = process_event

    # Sayfayı yükle
    driver.get(webpage_url)

    # Ağ trafiğini bekleyin ve işleyin
    driver.implicitly_wait(10)  # Sayfanın tam yüklenmesini bekler
    driver.quit()

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