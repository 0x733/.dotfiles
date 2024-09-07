import logging
from playwright.sync_api import sync_playwright
import yt_dlp

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AdvancedLinkFinder:
    def __init__(self, url):
        self.url = url
        self.media_url = None

    def find_with_playwright(self):
        """
        Playwright kullanarak sayfadaki medya linklerini bulur.
        """
        logging.info(f"Using Playwright to extract media links from: {self.url}")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(self.url)

                # Sayfanın tam olarak yüklenmesini bekliyoruz (örn. JavaScript ile yüklenen içerikler)
                page.wait_for_timeout(5000)  # 5 saniye bekliyoruz, gerekirse ayarlanabilir

                # Tüm sayfadaki linkleri alıyoruz
                links = page.locator("a")

                # HLS (m3u8) veya diğer medya uzantılarını arıyoruz
                media_links = []
                for link in links.element_handles():
                    href = link.get_attribute("href")
                    if href and (".m3u8" in href or ".mpd" in href or href.endswith(('.mp4', '.mkv'))):
                        media_links.append(href)

                browser.close()

                if media_links:
                    self.media_url = media_links[0]  # İlk medya linkini kullanıyoruz
                    logging.info(f"Media URL found with Playwright: {self.media_url}")
                    return self.media_url
                else:
                    logging.warning("No media URL found with Playwright.")
                    return None
        except Exception as e:
            logging.error(f"Error using Playwright: {e}")
            return None

    def find_with_yt_dlp(self, url=None):
        """
        yt-dlp kullanarak web sayfasından medya linklerini bulur.
        Eğer 'url' parametresi verilmezse, sınıfa atanmış olan URL kullanılır.
        """
        if url is None:
            url = self.url

        logging.info(f"Using yt-dlp to extract media links from: {url}")
        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,  # Yalnızca URL'yi çıkarmak istiyoruz, indirmeyeceğiz
                'force_generic_extractor': True,  # Bazı siteler için generic extractor'ı zorla
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'url' in info:
                    media_url = info['url']
                    logging.info(f"Media URL found with yt-dlp: {media_url}")
                    return media_url
                else:
                    logging.warning(f"No media URL found with yt-dlp for {url}.")
                    return None
        except Exception as e:
            logging.error(f"Error using yt-dlp: {e}")
            return None

    def recursive_media_finder(self, url=None, depth=2):
        """
        Medya linkini tekrar tekrar yakalamak için recursive yakalama yapar.
        'depth' parametresi, kaç defa tekrar yakalamaya çalışacağını belirtir.
        """
        if depth == 0:
            logging.warning("Maximum recursion depth reached. No media link found.")
            return None

        media_url = self.find_with_yt_dlp(url)
        if media_url:
            if ".m3u8" in media_url or ".mpd" in media_url or media_url.endswith(('.mp4', '.mkv')):
                # Eğer medya formatı yakalanmışsa, işlemi durdur ve sonucu geri dön.
                return media_url
            else:
                logging.info(f"Recursing into: {media_url}")
                # Eğer hala medya formatı değilse, bu URL'yi de işleyerek tekrar medya araması yap.
                return self.recursive_media_finder(media_url, depth - 1)
        else:
            logging.warning(f"Could not find media link at {url}")
            return None

    def download_or_play_media(self):
        """
        Bulunan medya URL'sini ya oynatır ya da indirir.
        """
        # İlk olarak Playwright ile deniyoruz
        media_url = self.find_with_playwright()

        if media_url:
            play = input(f"Do you want to play or download the media? (play/download): ").strip().lower()
            if play == "play":
                self.play_with_yt_dlp(media_url)
            elif play == "download":
                self.download_with_yt_dlp(media_url)
            else:
                logging.warning("Invalid option selected.")
        else:
            logging.error("No media URL found after Playwright search.")

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


# Main script
if __name__ == "__main__":
    webpage_url = input("Enter webpage URL to search for media stream: ")
    parser = AdvancedLinkFinder(webpage_url)

    # Playwright ile medya araması yap
    parser.download_or_play_media()