import requests
import webbrowser
import json
import tempfile
import os
import time

def sorgula_ve_html_olustur(bbk_kod):
    """
    Verilen BBK kodunu kullanarak altyapı sorgusu yapar, flexList'i ayrıştırır ve sonucu HTML formatında gösterir.

    Args:
        bbk_kod (str): Sorgulanacak bina bilgi kodu.
    """

    sorgu_url = f"https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod={bbk_kod}&datatype=checkAddress"
    yanit = requests.get(sorgu_url)

    if yanit.status_code == 200:
        veri = yanit.json()

        # flexList'i ayrıştır
        flex_list_verisi = veri.get("flexList", [])

        # HTML oluşturma
        html_icerik = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>BBK Sorgulama Sonucu</title>
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
            </style>
        </head>
        <body>
            <h1>BBK Sorgulama Sonucu</h1>
            <h2>flexList Verisi</h2>
            <table>
                <tr>
                    <th>Anahtar</th>
                    <th>Değer</th>
                </tr>
        """

        for item in flex_list_verisi:
            for key, value in item.items():
                html_icerik += f"<tr><td>{key}</td><td>{value}</td></tr>"

        html_icerik += """
            </table>
        </body>
        </html>
        """

        # Geçici HTML dosyası oluştur ve yaz
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as gecici_dosya:
            gecici_dosya.write(html_icerik.encode("utf-8"))

        # HTML dosyasını tarayıcıda aç
        webbrowser.open(gecici_dosya.name)

        # Tarayıcıyı kapatmak için bir süre bekle (örneğin 5 saniye)
        time.sleep(5)  
        os.remove(gecici_dosya.name)

    else:
        print("Sorgulama başarısız oldu. Lütfen BBK kodunu kontrol edin veya daha sonra tekrar deneyin.")

# Kullanıcıdan BBK kodunu al
bbk_kod = input("Lütfen sorgulamak istediğiniz BBK kodunu girin: ")
sorgula_ve_html_olustur(bbk_kod)