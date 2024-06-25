import subprocess
import json
import decimal

def run_speedtest():
    """Speedtest-cli ile hız testi yapar ve sonuçları döndürür."""
    try:
        result = subprocess.run(
            ["speedtest-cli", "--json"],  # JSON formatında çıktı al
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Hata: {e}")
        return None

def analyze_results(results):
    """Hız testi sonuçlarını analiz eder ve kullanıcıya sunar."""
    if results:
        # Decimal kullanarak daha hassas hesaplamalar
        download = decimal.Decimal(results["download"]) * 8 / decimal.Decimal(1e6)  # Bps to Mbps
        upload = decimal.Decimal(results["upload"]) * 8 / decimal.Decimal(1e6)
        ping = results["ping"]
        server = results["server"]["name"]

        print("\nHız Testi Sonuçları:")
        print(f"  Sunucu: {server}")
        print(f"  İndirme Hızı: {download:.4f} Mbps")  # 4 ondalık basamak
        print(f"  Yükleme Hızı: {upload:.4f} Mbps")
        print(f"  Ping: {ping:.2f} ms")

        # SQM Hesaplama (Opsiyonel)
        percentages = [90, 85, 80]
        for percent in percentages:
            sqm_download = download * percent / 100
            sqm_upload = upload * percent / 100
            print(f"\nÖnerilen SQM Ayarları ({percent}%):")
            print(f"  İndirme: {sqm_download:.2f} Kbps")  # 2 ondalık basamak
            print(f"  Yükleme: {sqm_upload:.2f} Kbps")

def main():
    """Ana fonksiyon: Hız testi yapar ve sonuçları analiz eder."""
    results = run_speedtest()
    analyze_results(results)

if __name__ == "__main__":
    main()