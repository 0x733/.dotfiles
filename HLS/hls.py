import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# Logger yapılandırması
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

class VideoScraper:
    def __init__(self, url, proxy=None):
        self.url = url
        self.proxy = proxy
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        options = uc.ChromeOptions()
        
        # Rastgele bir tarayıcı başlığı ekleyin
        options.add_argument(f'user-agent={self.get_random_user_agent()}')
        
        # Tarayıcı pencere boyutu ayarlayın
        options.add_argument('--window-size=1920,1080')
        
        # Sandbox ve Dev/SHM kullanımlarını devre dışı bırakın
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Proxy ayarlamak isteğe bağlıdır
        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')
            logging.info(f'Proxy kullanılıyor: {self.proxy}')

        # Tarayıcıyı başlatın
        driver = uc.Chrome(options=options)
        
        # Performans logları açın (XHR isteklerini yakalamak için)
        driver.command_executor._commands['getLog'] = ('POST', '/session/$sessionId/log')
        logging.info("Tarayıcı başlatıldı ve performans logları etkinleştirildi.")
        
        return driver

    def get_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
        ]
        user_agent = random.choice(user_agents)
        logging.info(f'Kullanılan User-Agent: {user_agent}')
        return user_agent

    def disable_webrtc(self):
        self.driver.execute_script("""
            var getUserMedia = navigator.mediaDevices.getUserMedia;
            navigator.mediaDevices.getUserMedia = function() {
                return new Promise(function(resolve, reject) {
                    reject(new Error("WebRTC is disabled"));
                });
            }
        """)
        logging.info("WebRTC devre dışı bırakıldı.")

    def manipulate_fingerprint(self):
        self.driver.execute_script("""
            const getContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function() {
                return null;
            };

            const getChannelData = AudioBuffer.prototype.getChannelData;
            AudioBuffer.prototype.getChannelData = function() {
                return new Float32Array(44100);
            };

            Object.defineProperty(screen, 'width', {
                get: function() { return 1920; }
            });
            Object.defineProperty(screen, 'height', {
                get: function() { return 1080; }
            });
        """)
        logging.info("Tarayıcı parmak izi manipüle edildi.")

    def clear_cookies(self):
        self.driver.delete_all_cookies()
        logging.info("Çerezler temizlendi.")

    def human_like_mouse_movements(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(element, random.randint(-50, 50), random.randint(-50, 50))

        for _ in range(random.randint(3, 7)):
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            actions.move_by_offset(x_offset, y_offset)
            actions.pause(random.uniform(0.1, 0.5))

        actions.move_to_element(element).click().perform()
        logging.info("Fare hareketleri ve tıklamalar simüle edildi.")

    def get_xhr_requests(self):
        logs = self.driver.get_log('performance')
        video_links = []
        for log in logs:
            log_message = log["message"]
            if "m3u8" in log_message or "mp4" in log_message or "mpd" in log_message:
                start = log_message.find("url") + 6
                end = log_message.find("\"", start)
                video_url = log_message[start:end]
                video_links.append(video_url)

        logging.info(f"{len(video_links)} video bağlantısı bulundu.")
        return video_links

    def scrape(self):
        # Sayfayı başlatın ve gerekli adımları gerçekleştirin
        self.driver.get(self.url)
        logging.info(f"Sayfa yüklendi: {self.url}")
        
        time.sleep(random.uniform(3, 5))  # Rastgele gecikme

        # WebRTC ve parmak izi manipülasyonları
        self.disable_webrtc()
        self.manipulate_fingerprint()

        # Çerezleri temizleyin
        self.clear_cookies()

        # Sayfada insan davranışıyla gezinme
        element = self.driver.find_element(By.TAG_NAME, 'body')
        self.human_like_mouse_movements(element)

        # XHR üzerinden video linklerini yakalayın
        video_links = self.get_xhr_requests()

        # Video bağlantılarını döndürün
        if video_links:
            logging.info("Bulunan video URL'leri:")
            for link in video_links:
                logging.info(link)
        else:
            logging.warning("Video bağlantısı bulunamadı.")
        
        # Tarayıcıyı kapatın
        self.driver.quit()
        logging.info("Tarayıcı kapatıldı.")

# Örnek kullanım
if __name__ == "__main__":
    url = "https://www.example.com"
    scraper = VideoScraper(url)
    scraper.scrape()