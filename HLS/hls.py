import time
import random
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# Logger configuration
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

class VideoScraper:
    def __init__(self, url, proxy=None, max_retries=3):
        self.url = url
        self.proxy = proxy
        self.max_retries = max_retries
        self.driver = None
        try:
            self.driver = self.initialize_driver()
        except WebDriverException as e:
            logging.error(f"Driver initialization failed: {e}")
            raise

    def initialize_driver(self):
        options = uc.ChromeOptions()

        # Random browser user-agent
        options.add_argument(f'user-agent={self.get_random_user_agent()}')

        # Window size
        options.add_argument('--window-size=1920,1080')

        # Disable sandbox and dev/shm usage
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Headless mode for performance
        options.add_argument('--headless')

        # Optional: Set up proxy
        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')
            logging.info(f'Using proxy: {self.proxy}')

        try:
            # Launch browser
            driver = uc.Chrome(options=options)
            logging.info("Browser launched.")
            return driver
        except WebDriverException as e:
            logging.error(f"Error launching browser: {e}")
            raise

    def get_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
        ]
        user_agent = random.choice(user_agents)
        logging.info(f'User-Agent set to: {user_agent}')
        return user_agent

    def disable_webrtc(self):
        try:
            self.driver.execute_script("""
                var getUserMedia = navigator.mediaDevices.getUserMedia;
                navigator.mediaDevices.getUserMedia = function() {
                    return new Promise(function(resolve, reject) {
                        reject(new Error("WebRTC is disabled"));
                    });
                }
            """)
            logging.info("WebRTC disabled.")
        except WebDriverException as e:
            logging.error(f"Error disabling WebRTC: {e}")

    def manipulate_fingerprint(self):
        try:
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
            logging.info("Browser fingerprint manipulated.")
        except WebDriverException as e:
            logging.error(f"Error manipulating fingerprint: {e}")

    def clear_cookies(self):
        try:
            self.driver.delete_all_cookies()
            logging.info("Cookies cleared.")
        except WebDriverException as e:
            logging.error(f"Error clearing cookies: {e}")

    def human_like_mouse_movements(self, element):
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(element, random.randint(-50, 50), random.randint(-50, 50))

            for _ in range(random.randint(3, 7)):
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-100, 100)
                actions.move_by_offset(x_offset, y_offset)
                actions.pause(random.uniform(0.1, 0.5))

            actions.move_to_element(element).click().perform()
            logging.info("Human-like mouse movements and clicks simulated.")
        except NoSuchElementException as e:
            logging.error(f"Element not found for human-like movements: {e}")
        except WebDriverException as e:
            logging.error(f"Error during mouse movement simulation: {e}")

    def scrape(self):
        retries = 0
        while retries < self.max_retries:
            try:
                # Load page and perform necessary actions
                self.driver.get(self.url)
                logging.info(f"Page loaded: {self.url}")

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )

                # Random delay
                time.sleep(random.uniform(2, 4))

                # WebRTC and fingerprint manipulations
                self.disable_webrtc()
                self.manipulate_fingerprint()

                # Clear cookies
                self.clear_cookies()

                # Simulate human behavior on the page
                element = self.driver.find_element(By.TAG_NAME, 'body')
                self.human_like_mouse_movements(element)

                # Log success and break
                logging.info("Scraping completed successfully.")
                break

            except (TimeoutException, WebDriverException) as e:
                logging.error(f"Error during scraping: {e}. Retrying...")
                retries += 1
                time.sleep(2)  # Short delay before retry

        finally:
            if self.driver:
                self.driver.quit()
                logging.info("Browser closed.")

# Example usage
if __name__ == "__main__":
    url = input("Please enter the URL to scrape: ")  # Taking URL input from the user
    scraper = VideoScraper(url)
    scraper.scrape()