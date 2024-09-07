from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_media_urls(webpage_url):
    # Tarayıcı seçenekleri
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Google Chrome'un tam yolu
    chrome_options.add_argument("--headless")  # Tarayıcı arka planda çalışsın
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ChromeDriver'ın yolu
    service = Service(executable_path='/usr/bin/chromedriver')

    # Selenium ile ChromeDriver başlat
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Sayfayı yükle
    driver.get(webpage_url)

    # Belirli bir elementin yüklenmesini bekle (örneğin video etiketi)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
    except:
        print("Video elementi yüklenmedi.")
    
    # Medya dosyası URL'lerini bul
    media_urls = []
    for request in driver.requests:
        url = request.url
        if is_media_url(url):
            media_urls.append(url)

    driver.quit()
    return media_urls