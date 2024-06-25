import subprocess
import json
import decimal
import statistics

def run_speedtest(server_id=None):
    """Speedtest-cli ile hız testi yapar. İsteğe bağlı olarak sunucu ID'si alır."""
    command = ["speedtest-cli", "--json"]
    if server_id:
        command.extend(["--server", server_id])
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Hata: {e}")
        return None

def analyze_results(results):
    """Hız testi sonuçlarını analiz eder ve kullanıcıya sunar."""
    if results:
        download_bps = decimal.Decimal(results["download"])
        upload_bps = decimal.Decimal(results["upload"])
        ping = results["ping"]
        server = results["server"]["name"]

        # Hız birimlerini hesapla (Bps, Kbps, Mbps, Gbps)
        download = {
            "Bps": download_bps,
            "Kbps": download_bps / 1024,
            "Mbps": download_bps / 1e6,
            "Gbps": download_bps / 1e9,
        }
        upload = {
            "Bps": upload_bps,
            "Kbps": upload_bps / 1024,
            "Mbps": upload_bps / 1e6,
            "Gbps": upload_bps / 1e9,
        }

        print("\nHız Testi Sonuçları:")
        print(f"  Sunucu: {server}")
        print(f"  Ping: {ping:.2f} ms")
        print("\n  İndirme Hızı:")
        for unit, value in download.items():
            print(f"    {unit}: {value:.4f}")
        print("\n  Yükleme Hızı:")
        for unit, value in upload.items():
            print(f"    {unit}: {value:.4f}")

        # SQM Hesaplama (Opsiyonel)
        percentages = [90, 85, 80]
        for percent in percentages:
            sqm_download = download["Kbps"] * percent / 100
            sqm_upload = upload["Kbps"] * percent / 100
            print(f"\nÖnerilen SQM Ayarları ({percent}%):")
            print(f"  İndirme: {sqm_download:.2f} Kbps")
            print(f"  Yükleme: {sqm_upload:.2f} Kbps")

def choose_server():
    """Kullanıcının sunucu seçmesine veya otomatik olarak en iyi sunucuyu bulmasına izin verir."""
    choice = input("Sunucu seçmek ister misiniz? (e/h): ")
    if choice.lower() == "e":
        servers = get_server_list()
        if not servers:
            print("Sunucu listesi alınamadı. Lütfen daha sonra tekrar deneyin.")
            return None

        for i, server in enumerate(servers):
            print(f"{i+1}. {server['name']} ({server['sponsor']}) - {server['country']}")
        server_index = int(input("Sunucu numarasını girin: ")) - 1
        return servers[server_index]["id"]
    else:
        print("En iyi sunucu otomatik olarak seçiliyor...")
        return find_best_server()

def get_server_list():
    """Speedtest sunucularını listeler ve döndürür."""
    try:
        result = subprocess.run(
            ["speedtest-cli", "--list"],
            capture_output=True,
            text=True,
        )

        # Çıktıyı ayrıştırma (parsing)
        servers = []
        for line in result.stdout.splitlines()[1:]:  # İlk satırı atla (başlık)
            parts = line.split()
            if len(parts) >= 6:
                server_id, sponsor, name, country, distance, latency, _ = parts
                servers.append({
                    "id": server_id,
                    "sponsor": sponsor,
                    "name": name,
                    "country": country,
                    "distance": distance,
                    "latency": latency,
                })
        return servers

    except subprocess.CalledProcessError as e:
        print(f"Hata: Sunucu listesi alınamadı: {e}")
        return []

def find_best_server():
    """Ping sürelerine göre en iyi sunucuyu bulur."""
    servers = get_server_list()
    best_server = min(servers, key=lambda x: x["latency"])
    return best_server["id"]

def calculate_jitter(server_ip):
    """Belirtilen sunucuya ping atarak jitter değerini hesaplar."""
    try:
        result = subprocess.run(
            ["ping", "-c", "10", server_ip],  # 10 kez ping at
            capture_output=True,
            text=True,
        )
        times = []
        for line in result.stdout.splitlines():
            if "time=" in line:
                time_str = line.split("time=")[1].split()[0]
                times.append(float(time_str))
        if times:
            return statistics.stdev(times)
        else:
            return None
    except subprocess.CalledProcessError:
        print(f"Jitter hesaplanırken hata oluştu.")
        return None

def calculate_packet_loss(server_ip):
    """Belirtilen sunucuya ping atarak paket kaybı yüzdesini hesaplar."""
    try:
        result = subprocess.run(
            ["ping", "-c", "10", server_ip],
            capture_output=True,
            text=True,
        )
        for line in result.stdout.splitlines():
            if "packet loss" in line:
                loss_str = line.split("packet loss")[0].split()[-1][:-1]
                return float(loss_str)
        return 0.0  # Paket kaybı yoksa 0 döndür
    except subprocess.CalledProcessError:
        print(f"Paket kaybı hesaplanırken hata oluştu.")
        return None

def save_results(results, filename="hiz_testi_sonuclari.json"):
    """Sonuçları JSON dosyasına kaydeder."""
    try:
        with open(filename, "a") as f:
            json.dump(results, f)
            f.write("\n")  # Her testi ayrı satıra yaz
    except Exception as e:
        print(f"Sonuçlar kaydedilirken hata oluştu: {e}")

def main():
    """Ana fonksiyon: Hız testi yapar, sonuçları analiz eder ve kaydeder."""
    server_id = choose_server()
    if server_id is None:
        print("Hız testi yapılamıyor. Lütfen sunucu seçiminizi kontrol edin veya daha sonra tekrar deneyin.")
        return

    results = run_speedtest(server_id)
    if results:
        analyze_results(results)
        server_ip = results["server"]["ip"]
        jitter = calculate_jitter(server_ip)
        packet_loss = calculate_packet_loss(server_ip)
        results["jitter"] = jitter
        results["packetLoss"] = packet_loss
        print(f"\nJitter: {jitter:.2f} ms (eğer None ise jitter hesaplanamamıştır)")
        print(f"Paket Kaybı: {packet_loss:.2f}%")
        save_results(results)

if __name__ == "__main__":
    main()