import speedtest
import json
from datetime import datetime

def hiz_testi_yap():
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    st_sonuclari = st.results.dict()
    indirme_hizi_mbps = st_sonuclari["download"] / 1_000_000  # Mbps'ye dönüştürme
    yukleme_hizi_mbps = st_sonuclari["upload"] / 1_000_000  # Mbps'ye dönüştürme
    gecikme = st_sonuclari["ping"]
    return indirme_hizi_mbps, yukleme_hizi_mbps, gecikme

def hiz_testi_sonuclarini_goster(indirme_hizi_mbps, yukleme_hizi_mbps):
    indirme_hizi_kbps = indirme_hizi_mbps * 1_000  # kbps'ye dönüştürme
    yukleme_hizi_kbps = yukleme_hizi_mbps * 1_000  # kbps'ye dönüştürme

    sonuclar = {
        "İndirme Hızı": {
            "Mbps": f"{indirme_hizi_mbps:.2f}",
            "Azaltılmış": {},
            "Artırılmış": {}
        },
        "Yükleme Hızı": {
            "Mbps": f"{yukleme_hizi_mbps:.2f}",
            "Azaltılmış": {},
            "Artırılmış": {}
        }
    }

    # İndirme Hızı Yüzde Sonuçları (80% ile 90% arası, %5 artışlarla)
    for yuzde in range(80, 91, 5):
        sonuclar["İndirme Hızı"]["Azaltılmış"][f"{yuzde}%"] = f"{indirme_hizi_mbps * (yuzde / 100):.2f} Mbps"
        sonuclar["İndirme Hızı"]["Artırılmış"][f"{yuzde}%"] = f"{indirme_hizi_mbps * ((100 + yuzde) / 100):.2f} Mbps"

    # Yükleme Hızı Yüzde Sonuçları (80% ile 90% arası, %5 artışlarla)
    for yuzde in range(80, 91, 5):
        sonuclar["Yükleme Hızı"]["Azaltılmış"][f"{yuzde}%"] = f"{yukleme_hizi_mbps * (yuzde / 100):.2f} Mbps"
        sonuclar["Yükleme Hızı"]["Artırılmış"][f"{yuzde}%"] = f"{yukleme_hizi_mbps * ((100 + yuzde) / 100):.2f} Mbps"

    # İndirme Hızı Yüzde Sonuçları (80% ile 90% arası, %5 artışlarla) kbps cinsinden
    for yuzde in range(80, 91, 5):
        sonuclar["İndirme Hızı"]["Azaltılmış"][f"{yuzde}% kbps"] = f"{indirme_hizi_kbps * (yuzde / 100):.2f} kbps"
        sonuclar["İndirme Hızı"]["Artırılmış"][f"{yuzde}% kbps"] = f"{indirme_hizi_kbps * ((100 + yuzde) / 100):.2f} kbps"

    # Yükleme Hızı Yüzde Sonuçları (80% ile 90% arası, %5 artışlarla) kbps cinsinden
    for yuzde in range(80, 91, 5):
        sonuclar["Yükleme Hızı"]["Azaltılmış"][f"{yuzde}% kbps"] = f"{yukleme_hizi_kbps * (yuzde / 100):.2f} kbps"
        sonuclar["Yükleme Hızı"]["Artırılmış"][f"{yuzde}% kbps"] = f"{yukleme_hizi_kbps * ((100 + yuzde) / 100):.2f} kbps"

    return sonuclar

def ana_program():
    baslangic_zamani = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Test başladı: {baslangic_zamani}")

    # Hız testini çalıştır
    indirme_hizi_mbps, yukleme_hizi_mbps, gecikme = hiz_testi_yap()

    hiz_testi_sonuclari = {
        "İndirme Hızı": f"{indirme_hizi_mbps:.2f} Mbps",
        "Yükleme Hızı": f"{yukleme_hizi_mbps:.2f} Mbps",
        "Gecikme": f"{gecikme:.2f} ms",
        **hiz_testi_sonuclarini_goster(indirme_hizi_mbps, yukleme_hizi_mbps)
    }

    print(json.dumps(hiz_testi_sonuclari, indent=4, ensure_ascii=False))

    bitis_zamani = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Test bitti: {bitis_zamani}")

if __name__ == "__main__":
    ana_program()