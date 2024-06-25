import subprocess
import json

def find_best_server():
    try:
        # En uygun sunucuyu bulma
        result = subprocess.run(['/usr/bin/speedtest-go', '--list'], capture_output=True, text=True)
        output_lines = result.stdout.strip().split('\n')
        
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
            print("En uygun speedtest sunucusu bulunamadı. Lütfen tekrar deneyin veya /usr/bin/speedtest-go komutunu kontrol edin.")
            return None
    
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e}")
        return None

def run_speedtest(server_id):
    try:
        # Hız testi yapma
        result = subprocess.run(['/usr/bin/speedtest-go', '--server', server_id], capture_output=True, text=True)
        speedtest_output = result.stdout.strip()
        
        # Parse the speedtest output
        speedtest_data = json.loads(speedtest_output)
        download_speed = speedtest_data['Download'] * 1000  # Mbps to Kbps
        upload_speed = speedtest_data['Upload'] * 1000     # Mbps to Kbps
        
        print(f"Download Hızı: {download_speed:.2f} Kbps")
        print(f"Upload Hızı: {upload_speed:.2f} Kbps")
        
        # Yüzdelik oranlar için SQM hesaplama
        percentages = [90, 85, 80]
        for percent in percentages:
            sqm_download = int(download_speed * percent / 100)
            sqm_upload = int(upload_speed * percent / 100)
            print(f"Önerilen SQM için ayarlanacak Download Hızı ({percent}%): {sqm_download} Kbps")
            print(f"Önerilen SQM için ayarlanacak Upload Hızı ({percent}%): {sqm_upload} Kbps")
    
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Hata: {e}")

def main():
    # En uygun sunucuyu bul
    server_id = find_best_server()
    
    if server_id:
        print(f"En düşük gecikme sunucusu: {server_id}")
        # Hız testi yap
        run_speedtest(server_id)

if __name__ == "__main__":
    main()