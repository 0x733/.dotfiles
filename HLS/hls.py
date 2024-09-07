import yt_dlp
import requests
import logging
import os
import subprocess
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

    def find_with_yt_dlp(self):
        """
        yt-dlp kullanarak web sayfasından medya linklerini bulur.
        """
        logging.info(f"Using yt-dlp to extract media links from: {self.url}")
        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,  # Yalnızca URL'yi çıkarmak istiyoruz, indirmeyeceğiz
                'force_generic_extractor': True,  # Bazı siteler için generic extractor'ı zorla
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                if 'url' in info:
                    self.media_url = info['url']
                    logging.info(f"Media URL found: {self.media_url}")
                else:
                    logging.warning("No media URL found with yt-dlp.")
        except Exception as e:
            logging.error(f"Error using yt-dlp: {e}")
            return False
        return True

    def find_with_selenium(self):
        """
        Selenium kullanarak tarayıcı üzerinden HLS linklerini bulur.
        """
        logging.info(f"Using Selenium to extract media links from: {self.url}")
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
            service = Service(executable_path='/usr/bin/chromedriver')  # ChromeDriver yolu

            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(self.url)

            # Sayfadaki .m3u8 linklerini buluyoruz
            media_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '.m3u8')]")
            if media_elements:
                self.media_url = media_elements[0].get_attribute('href')
                logging.info(f"Media URL found with Selenium: {self.media_url}")
            else:
                logging.warning("No media URL found with Selenium.")
            driver.quit()
        except Exception as e:
            logging.error(f"Error using Selenium: {e}")
            return False
        return True

    def download_with_mpv(self):
        """
        Bulunan HLS linkini MPV kullanarak indirir veya oynatır.
        """
        if not self.media_url:
            logging.error("No media URL available to play or download.")
            return False

        play = input(f"Do you want to play or download the media? (play/download): ").strip().lower()
        if play == "play":
            self.play_with_mpv(self.media_url)
        elif play == "download":
            self.download_with_yt_dlp(self.media_url)
        else:
            logging.warning("Invalid option selected.")
        return True

    def play_with_mpv(self, media_url):
        """
        MPV kullanarak bulunan medya linkini oynatır.
        """
        try:
            logging.info(f"Playing media with MPV: {media_url}")
            subprocess.run(['mpv', media_url], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error occurred while playing the media with MPV: {e}")

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


# Main script
if __name__ == "__main__":
    webpage_url = input("Enter webpage URL to search for media stream: ")
    parser = AdvancedLinkFinder(webpage_url)

    # Öncelikle yt-dlp ile deniyoruz
    if not parser.find_with_yt_dlp():
        # Son çare Selenium ile deniyoruz
        parser.find_with_selenium()

    if parser.media_url:
        parser.download_with_mpv()
    else:
        logging.error("No media URL found with any method.")