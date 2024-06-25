import subprocess
import json

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
        download = results["download"] / 1e6  # Bps to Mbps
        upload = results["upload"] / 1e6
        ping = results["ping"]
        server = results["server"]["name"]

        print("\nHız Testi Sonuçları:")
        print(f"  Sunucu: {server}")
        print(f"  İndirme Hızı: {download:.2f} Mbps")
        print(f"  Yükleme Hızı: {upload:.2f} Mbps")
        print(f"  Ping: {ping:.2f} ms")

        # SQM Hesaplama (Opsiyonel)
        percentages = [90, 85, 80]
        for percent in percentages:
            sqm_download = int(download * percent / 100)
            sqm_upload = int(upload * percent / 100)
            print(f"\nÖnerilen SQM Ayarları ({percent}%):")
            print(f"  İndirme: {sqm_download} Kbps")
            print(f"  Yükleme: {sqm_upload} Kbps")

def main():
    """Ana fonksiyon: Hız testi yapar ve sonuçları analiz eder."""
    results = run_speedtest()
    analyze_results(results)

if __name__ == "__main__":
    main()