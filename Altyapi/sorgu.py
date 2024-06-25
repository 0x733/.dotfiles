import requests
from bs4 import BeautifulSoup
from json2html import json2html
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

bbk = "0000000000"
url_bbk = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk}&datatype=checkAddress"
url_scrape = "https://goknet.com.tr/internet-altyapi-sorgulama/"

def scrape_table(driver):
    try:
        driver.get(url_scrape)

        # Bekleme süresi ekleyerek web sitesinin tam olarak yüklenmesini sağla
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tt-tab")))

        # 'tt-tab' class'ına sahip tabloyu bul
        table = driver.find_element(By.CLASS_NAME, "tt-tab")

        if table:
            # Tabloyu HTML olarak al
            table_html = table.get_attribute("outerHTML")
            return table_html
        else:
            print("Belirtilen tablo bulunamadı.")
            return None

    except Exception as e:
        print(f"Hata: {e}")
        return None

def check_port_status(driver):
    try:
        driver.get(url_bbk)

        # JavaScript ile JSON verisini al
        json_data_str = driver.execute_script("""
            return fetch(arguments[0])
                .then(response => response.json())
                .then(data => JSON.stringify(data))
                .catch(error => console.error('Error:', error));
        """, url_bbk)

        # String formatındaki JSON verisini Python dictionary'sine dönüştür
        json_data = json.loads(json_data_str)

        # Port durumu bilgilerini al
        port_value = json_data.get('6', {}).get('flexList', {}).get('flexList', [])[2].get('value', '')
        error_code = json_data.get('6', {}).get('hataKod', '')
        message = json_data.get('6', {}).get('hataMesaj', '')

        port_status = 'VAR' if port_value == '1' else 'YOK'

        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")

        log_message = f"[{current_time}] Port Durumu: {port_status}, Hata Kodu: {error_code}, Mesaj: {message}"
        print(log_message)

        # JSON verisini HTML'e dönüştür
        html_table = json2html.convert(json=json_data)

        # WebDriver üzerinden tabloyu kazı
        scraped_table = scrape_table(driver)

        if scraped_table:
            # Ana HTML dosyasını oluştur
            html_content = f"""
            <html>
            <head><title>Port Durumu</title></head>
            <body>
            <h2>Port Durumu Bilgileri</h2>
            {html_table}
            <h2>Kazınan Tablo</h2>
            {scraped_table}
            </body>
            </html>
            """

            # HTML dosyasını kaydet
            filename = f"port_status_{current_time}.html"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(html_content)
                print(f"HTML dosyası kaydedildi: {filename}")

            return True

    except Exception as e:
        print(f"Hata: {e}")
        return False

    finally:
        driver.quit()

# Chrome WebDriver'ı başlat
options = Options()
options.add_argument("--headless")  # Arka planda çalıştırma
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

# Port durumu kontrolü ve kazıma işlemi yap
if check_port_status(driver):
    print("Program sonlandı.")