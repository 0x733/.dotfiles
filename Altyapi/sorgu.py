import json
import os
import tempfile
import webbrowser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from json2html import json2html

bbk = "0000000000"
url_bbk = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk}&datatype=checkAddress"

def fetch_json_data():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

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
            return None

        return json.loads(json_data_str)

    except Exception as e:
        print(f"Hata: {e}")
        return None

    finally:
        driver.quit()

def save_and_open_html(json_data):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    html_content = f"""
    <html>
    <head><title>JSON Verisi</title></head>
    <body>
    <h2>JSON Verisi</h2>
    {json2html.convert(json=json_data)}
    </body>
    </html>
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        tmp_file.write(html_content.encode('utf-8'))
        tmp_file_path = tmp_file.name
        print(f"HTML dosyası kaydedildi: {tmp_file_path}")

    webbrowser.open(f"file://{tmp_file_path}")

    input("HTML dosyasını kapatmak için Enter'a basın...")
    os.remove(tmp_file_path)
    print(f"HTML dosyası silindi: {tmp_file_path}")

json_data = fetch_json_data()

if json_data:
    save_and_open_html(json_data)
else:
    print("JSON verisi alınamadı veya işlenemedi.")