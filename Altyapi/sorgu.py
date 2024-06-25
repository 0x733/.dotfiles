import requests
from bs4 import BeautifulSoup
from json2html import json2html
from datetime import datetime, timedelta

bbk = "0000000000"
url_bbk = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk}&datatype=checkAddress"
url_scrape = "https://goknet.com.tr/internet-altyapi-sorgulama/"

def scrape_table():
    try:
        response = requests.get(url_scrape)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 'tt-tab' class'ına sahip tabloyu bul
        table = soup.find('table', class_='tt-tab')

        if table:
            # Tabloyu HTML olarak al
            table_html = str(table)
            return table_html
        else:
            print("Belirtilen tablo bulunamadı.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"İstek hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

    return None

def check_port_status():
    try:
        response = requests.get(url_bbk)
        response.raise_for_status()
        json_data = response.json()

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

        # Kazıma işleminden gelen HTML tablosunu al
        scraped_table = scrape_table()

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

    except requests.exceptions.RequestException as e:
        print(f"İstek hatası: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON ayrıştırma hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

    return False

if check_port_status():
    print("Program sonlandı.")