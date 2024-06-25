import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

bbk = "0000000000"
url_bbk = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk}&datatype=checkAddress"
url_scrape = "https://goknet.com.tr/internet-altyapi-sorgulama/"

def scrape_table(driver):
    try:
        driver.get(url_scrape)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "tt-tab")))

        table = driver.find_element(By.CLASS_NAME, "tt-tab")
        if table:
            table_html = table.get_attribute("outerHTML")
            return table_html
        else:
            print("Belirtilen tablo bulunamadı.")
            return None
    except Exception as e:
        print(f"Hata (scrape_table): {e}")
        return None

def check_port_status(driver):
    try:
        driver.get(url_bbk)

        json_data_str = driver.execute_script("""
            return fetch(arguments[0])
                .then(response => response.json())
                .then(data => JSON.stringify(data))
                .catch(error => {console.error('Fetch error:', error); return null;});
        """, url_bbk)

        if not json_data_str:
            print("JSON verisi alınamadı.")
            return False

        try:
            json_data = json.loads(json_data_str)
        except json.JSONDecodeError as e:
            print(f"JSON dönüştürme hatası: {e}")
            return False

        print("JSON Data:", json_data)

        port_value = json_data.get('6', {}).get('flexList', {}).get('flexList', [])[2].get('value', '')
        error_code = json_data.get('6', {}).get('hataKod', '')
        message = json_data.get('6', {}).get('hataMesaj', '')

        port_status = 'VAR' if port_value == '1' else 'YOK'

        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S")

        log_message = f"[{current_time}] Port Durumu: {port_status}, Hata Kodu: {error_code}, Mesaj: {message}"
        print(log_message)

        html_table = json2html.convert(json=json_data)

        scraped_table = scrape_table(driver)

        if scraped_table:
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

            filename = f"port_status_{current_time}.html"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(html_content)
                print(f"HTML dosyası kaydedildi: {filename}")

            return True

    except Exception as e:
        print(f"Hata (check_port_status): {e}")
        return False

    finally:
        driver.quit()

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

if check_port_status(driver):
    print("Program sonlandı.")