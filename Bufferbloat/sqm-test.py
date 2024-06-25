import subprocess
import json

def find_best_server():
    """En düşük gecikme süresine sahip sunucuyu bulur."""
    try:
        result = subprocess.run(
            ["/usr/bin/speedtest-go", "--list"],  # Komutun tam yolunu kullanın
            capture_output=True,
            text=True,
        )
        output_lines = result.stdout.strip().split("\n")

        best_server = None
        min_latency = None

        for line in output_lines:
            if line.startswith("  "):
                parts = line.split()
                if len(parts) >= 6:
                    server_id = parts[0]
                    latency = int(parts[4])
                    if min_latency is None or latency < min_latency:
                        min_latency = latency
                        best_server = server_id

        if best_server:
            return best_server
        else:
            raise Exception("Uygun sunucu bulunamadı.")

    except (subprocess.CalledProcessError, Exception) as e:
        print(f"Hata: {e}")
        return None

def run_speedtest(server_id):
    """Belirtilen sunucu ID'si ile hız testi yapar ve sonuçları analiz eder."""
    try:
        result = subprocess.run(
            ["/usr/bin/speedtest-go", "--server", server_id, "--json"],  # JSON çıktısı
            capture_output=True,
            text=True,
        )
        speedtest_data = json.loads(result.stdout)

        download_speed = speedtest_data["download"]["bandwidth"] * 8 / 1e6  # Bps to Mbps
        upload_speed = speedtest_data["upload"]["bandwidth"] * 8 / 1e6
        ping = speedtest_data["ping"]["latency"]

        print("\nHız Testi Sonuçları:")
        print(f"  İndirme Hızı: {download_speed:.2f} Mbps")
        print(f"  Yükleme Hızı: {upload_speed:.2f} Mbps")
        print(f"  Ping: {ping:.2f} ms")

        # SQM hesaplama
        percentages = [90, 85, 80]
        for percent in percentages:
            sqm_download = int(download_speed * percent / 100)
            sqm_upload = int(upload_speed * percent / 100)
            print(f"\nÖnerilen SQM Ayarları ({percent}%):")
            print(f"  İndirme: {sqm_download} Kbps")
            print(f"  Yükleme: {sqm_upload} Kbps")

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Hata: {e}")

def main():
    """Ana fonksiyon: Kullanıcıdan sunucu ID'si alır veya en iyi sunucuyu bulur ve hız testi yapar."""
    try:
        server_id = input(
            "Sunucu ID'sini girin (boş bırakırsanız en uygun sunucu bulunur): "
        )
        if not server_id:
            server_id = find_best_server()

        if server_id:
            run_speedtest(server_id)
        else:
            print("Geçerli bir sunucu ID'si bulunamadı.")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    main()