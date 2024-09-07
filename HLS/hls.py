import logging
import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AdvancedLinkFinder:
    def __init__(self, url):
        self.url = url
        self.media_url = None

    def find_with_selenium(self):
        """
        Selenium kullanarak tarayıcı üzerinden HLS, MP4 veya diğer medya linklerini bulur.
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

            # Sayfadaki tüm linkleri buluyoruz
            links = driver.find_elements(By.TAG_NAME, "a")
            media_links = []

            # HLS (m3u8) veya diğer medya uzantılarını arıyoruz
            for link in links:
                href = link.get_attribute("href")
                if href and (".m3u8" in href or ".mpd" in href or href.endswith(('.mp4', '.mkv'))):
                    media_links.append(href)

            driver.quit()

            if media_links:
                self.media_url = media_links[0]  # İlk medya linkini kullanıyoruz
                logging.info(f"Media URL found with Selenium: {self.media_url}")
                return self.media_url
            else:
                logging.warning("No media URL found with Selenium.")
                return None
        except Exception as e:
            logging.error(f"Error using Selenium: {e}")
            return None

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
        media_url = self.find_with_selenium()

        if media_url:
            play = input(f"Do you want to play or download the media? (play/download): ").strip().lower()
            if play == "play":
                self.play_with_yt_dlp(media_url)
            elif play == "download":
                self.download_with_yt_dlp(media_url)
            else:
                logging.warning("Invalid option selected.")
        else:
            logging.error("No media URL found after Selenium search.")


# Main script
if __name__ == "__main__":
    webpage_url = input("Enter webpage URL to search for media stream: ")
    parser = AdvancedLinkFinder(webpage_url)

    # Selenium ile medya araması yap
    parser.download_or_play_media()