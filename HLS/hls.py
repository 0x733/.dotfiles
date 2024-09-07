import re
import logging
import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AdvancedLinkFinder:
    def __init__(self, url):
        self.url = url
        self.media_url = None

    def find_with_selenium_and_regex(self):
        """
        Selenium kullanarak sayfanın HTML kaynağını alır ve regex ile medya linklerini arar.
        """
        logging.info(f"Using Selenium to extract media links from: {self.url}")
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            service = Service(executable_path='/usr/bin/chromedriver')  # ChromeDriver yolu

            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(self.url)
            
            # Sayfanın tam olarak yüklenmesini bekliyoruz
            driver.implicitly_wait(10)

            # Sayfanın HTML kaynak kodunu alıyoruz
            page_source = driver.page_source
            driver.quit()

            # Regex kullanarak medya dosyalarını buluyoruz
            media_links = self.extract_media_links_with_regex(page_source)

            if media_links:
                self.media_url = media_links[0]  # İlk medya linkini kullanıyoruz
                logging.info(f"Media URL found with Selenium and Regex: {self.media_url}")
                return self.media_url
            else:
                logging.warning("No media URL found with Selenium and Regex.")
                return None
        except Exception as e:
            logging.error(f"Error using Selenium: {e}")
            return None

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

    def play_with_yt_dlp(self, media_url):
        """
        yt-dlp ile videoyu oynatır.
        """
        try:
            logging.info(f"Playing media with yt-dlp: {media_url}")
            ydl_opts = {
                'quiet': False,
                'noplaylist': True,  # Sadece bir dosya indir
                'format': 'best',    # En iyi kaliteyi seç
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([media_url])
        except Exception as e:
            logging.error(f"Error occurred while playing the media with yt-dlp: {e}")

    def download_with_yt_dlp(self, media_url):
        """
        yt-dlp kullanarak medya linkini indirir.
        """
        logging.info(f"Using yt-dlp to download media from: {media_url}")
        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': False,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([media_url])
        except Exception as e:
            logging.error(f"Error using yt-dlp to download media: {e}")
            return False
        return True

    def download_or_play_media(self):
        """
        Bulunan medya URL'sini ya oynatır ya da indirir.
        """
        media_url = self.find_with_selenium_and_regex()

        if media_url:
            play = input(f"Do you want to play or download the media? (play/download): ").strip().lower()
            if play == "play":
                self.play_with_yt_dlp(media_url)
            elif play == "download":
                self.download_with_yt_dlp(media_url)
            else:
                logging.warning("Invalid option selected.")
        else:
            logging.error("No media URL found after Selenium and Regex search.")


# Main script
if __name__ == "__main__":
    webpage_url = input("Enter webpage URL to search for media stream: ")
    parser = AdvancedLinkFinder(webpage_url)

    # Regex ve Selenium ile medya araması yap
    parser.download_or_play_media()