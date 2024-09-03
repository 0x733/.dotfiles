import subprocess
import json

def main():
    try:
        # Speedtest-cli command
        result = subprocess.run(['speedtest-cli', '--json'], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        # Conversion and calculations
        download_speed_mbps = data['download'] / 1e6  # Convert to Mbps
        upload_speed_mbps = data['upload'] / 1e6  # Convert to Mbps
        
        print(f"Mevcut Download Hızı: {download_speed_mbps:.2f} Mbps")
        print(f"Mevcut Upload Hızı: {upload_speed_mbps:.2f} Mbps")
        
        # Calculate kbps and adjust by 10%
        download_speed_adjusted_kbps = download_speed_mbps * 900  # Convert to kbps and reduce by 10%
        upload_speed_adjusted_kbps = upload_speed_mbps * 900  # Convert to kbps and reduce by 10%
        
        print(f"SQM için Ayarlanan Download Hızı: {download_speed_adjusted_kbps:.0f} kbps")
        print(f"SQM için Ayarlanan Upload Hızı: {upload_speed_adjusted_kbps:.0f} kbps")
        
        # Final output
        print("\nLütfen aşağıdaki değerleri OpenWRT cihazınıza manuel olarak girin:")
        print(f"Download Hızı: {int(download_speed_adjusted_kbps)} kbps")
        print(f"Upload Hızı: {int(upload_speed_adjusted_kbps)} kbps")
    
    except subprocess.CalledProcessError as e:
        print("Speedtest-cli komutu çalıştırılırken bir hata oluştu.")
    except json.JSONDecodeError as e:
        print("JSON verisi işlenirken bir hata oluştu.")
    except KeyError as e:
        print(f"Beklenmeyen veri formatı: {e}")
    except Exception as e:
        print(f"Bilinmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    main()