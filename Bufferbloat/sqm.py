import subprocess
import json
import sys
from typing import Dict, Tuple

def run_speedtest() -> Dict:
    try:
        result = subprocess.run(['speedtest-cli', '--json'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError:
        print("Hata: speedtest-cli çalıştırılamadı. Yüklü olduğundan emin olun.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Hata: Speedtest sonuçları işlenemedi.")
        sys.exit(1)

def calculate_speeds(data: Dict, adjustment_factor: float = 0.9) -> Tuple[float, float]:
    try:
        download_mbps = data['download'] / 1e6
        upload_mbps = data['upload'] / 1e6
        
        download_kbps = download_mbps * 1000 * adjustment_factor
        upload_kbps = upload_mbps * 1000 * adjustment_factor
        
        return download_mbps, upload_mbps, download_kbps, upload_kbps
    except KeyError as e:
        print(f"Hata: Gerekli veri bulunamadı: {e}")
        sys.exit(1)

def display_results(download_mbps: float, upload_mbps: float, 
                   download_kbps: float, upload_kbps: float) -> None:
    print("\n=== Hız Testi Sonuçları ===")
    print(f"Mevcut Download Hızı: {download_mbps:.2f} Mbps")
    print(f"Mevcut Upload Hızı: {upload_mbps:.2f} Mbps")
    
    print("\n=== SQM için Ayarlanmış Değerler ===")
    print(f"Download: {int(download_kbps)} kbps")
    print(f"Upload: {int(upload_kbps)} kbps")

def main():
    try:
        print("Hız testi başlatılıyor...")
        data = run_speedtest()
        speeds = calculate_speeds(data)
        display_results(*speeds)
        
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()