#!/usr/bin/env python3
import subprocess
import json

def main():
    try:
        # En uygun sunucuyu bulma
        best_server_output = subprocess.run(['speedtest-go', '--list'], capture_output=True, text=True)
        best_server_lines = best_server_output.stdout.strip().split('\n')
        
        best_server = None
        for line in best_server_lines:
            if 'best server' in line.lower():
                best_server = line.split(':')[1].strip()
                break
        
        if not best_server:
            print("En uygun speedtest sunucusu bulunamadı. Lütfen tekrar deneyin veya speedtest-go komutunu kontrol edin.")
            return
        
        # Hız testi yapma
        speedtest_output = subprocess.run(['speedtest-go', '--server', best_server], capture_output=True, text=True)
        
        # Parse the speedtest output
        try:
            speedtest_data = json.loads(speedtest_output.stdout)
            download_speed = speedtest_data['Download']
            upload_speed = speedtest_data['Upload']
            
            download_speed_kbps = download_speed * 1000
            upload_speed_kbps = upload_speed * 1000
            
            print(f"Download Hızı: {download_speed_kbps:.2f} Kbps")
            print(f"Upload Hızı: {upload_speed_kbps:.2f} Kbps")
            
            # Hızların yüzdelik oranlarını hesaplama
            percentages = [90, 85, 80]
            for percentage in percentages:
                sqm_download = int(download_speed_kbps * percentage / 100)
                sqm_upload = int(upload_speed_kbps * percentage / 100)
                print(f"Önerilen SQM için ayarlanacak Download Hızı ({percentage}%): {sqm_download} Kbps")
                print(f"Önerilen SQM için ayarlanacak Upload Hızı ({percentage}%): {sqm_upload} Kbps")
        
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Hız testi sonucu alınamadı veya işlenemedi: {e}")
    
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e}")
    

if __name__ == "__main__":
    main()