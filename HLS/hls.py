import re
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging

class AdvancedLinkFinder:
    def __init__(self, url):
        self.url = url
        self.media_url = None
        self.proxy = None

    def start_proxy(self):
        """
        BrowserMob Proxy'yi başlatır ve Selenium ile entegrasyonunu sağlar.
        """
        server = Server("/home/user/.dotfiles/HLS/browsermob-proxy-2.1.4/bin/browsermob-proxy")  # proxy yolunu doğru yapıya göre değiştirin
        server.start()
        self.proxy = server.create_proxy()
        return self.proxy

    def find_media_links(self):
        """
        Selenium ile sayfayı ziyaret eder ve proxy üzerinden ağ trafiğini izler.
        """
        proxy = self.start_proxy()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f'--proxy-server={proxy.proxy}')

        service = Service(executable_path='/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Ağ trafiğini izlemeye başla
        proxy.new_har("media", options={'captureContent': True})
        driver.get(self.url)

        # Har'ı al (Ağ trafiği yakalandı)
        har = proxy.har

        # Ağ trafiğinden medya linklerini çıkar
        media_links = []
        for entry in har['log']['entries']:
            url = entry['request']['url']
            if self.is_media_file(url):
                media_links.append(url)
            else:
                # HTML kaynağını kontrol et
                response_content = entry['response'].get('content', {}).get('text', '')
                extracted_links = self.extract_media_links_with_regex(response_content)
                media_links.extend(extracted_links)

        driver.quit()
        proxy.close()
        return media_links

    def extract_media_links_with_regex(self, html):
        """
        Verilen HTML içinde regex kullanarak medya linklerini arar.
        """
        # HTML etiketlerinde gömülü medya kaynaklarını arayan regex desenleri
        media_patterns = [
            r'<iframe[^>]+src=["\'](https?://[^"\']+)["\']',  # iframe src yakalama
            r'<video[^>]+src=["\'](https?://[^"\']+)["\']',   # video src yakalama
            r'<source[^>]+src=["\'](https?://[^"\']+)["\']',  # source etiketinde video src yakalama
            r'<embed[^>]+src=["\'](https?://[^"\']+)["\']',   # embed src yakalama
            r'(https?://[^\s]+\.m3u8)',  # HLS linki
            r'(https?://[^\s]+\.mpd)',   # DASH linki
            r'(https?://[^\s]+\.mp4)',   # MP4 dosyası
            r'(https?://[^\s]+\.mkv)'    # MKV dosyası
        ]

        media_links = []
        for pattern in media_patterns:
            matches = re.findall(pattern, html)
            media_links.extend(matches)

        return media_links

    def is_media_file(self, url):
        """
        Bir URL'nin doğrudan bir medya dosyası olup olmadığını kontrol eder.
        """
        media_file_extensions = ['.m3u8', '.mpd', '.mp4', '.mkv']
        return any(url.endswith(ext) for ext in media_file_extensions)


# Main script
if __name__ == "__main__":
    # Kullanıcıdan URL al
    webpage_url = input("Enter the webpage URL to search for media streams: ").strip()
    
    # AdvancedLinkFinder sınıfını başlat
    finder = AdvancedLinkFinder(webpage_url)

    # Medya linklerini bul ve ekrana yazdır
    media_links = finder.find_media_links()
    if media_links:
        for link in media_links:
            print(f"Found media link: {link}")
    else:
        print("No media links found.")