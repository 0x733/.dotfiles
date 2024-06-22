#!/bin/sh

# İnternet hız testi
echo "Hız testi yapılıyor..."
SPEEDTEST_OUTPUT=$(speedtest-cli --simple)

# Download ve Upload hızlarını çıkarma
DOWNLOAD_SPEED=$(echo "$SPEEDTEST_OUTPUT" | grep "Download" | awk '{print $2}')
UPLOAD_SPEED=$(echo "$SPEEDTEST_OUTPUT" | grep "Upload" | awk '{print $2}')

# Hızları Kbps cinsine çevirme (Speedtest-cli sonucu Mbps cinsindendir)
DOWNLOAD_SPEED_KBPS=$(echo "$DOWNLOAD_SPEED * 1000" | bc)
UPLOAD_SPEED_KBPS=$(echo "$UPLOAD_SPEED * 1000" | bc)

echo "Download Hızı: $DOWNLOAD_SPEED_KBPS Kbps"
echo "Upload Hızı: $UPLOAD_SPEED_KBPS Kbps"

# Hızların yüzdelik oranlarını hesaplama fonksiyonu
calculate_sqm() {
  local speed=$1
  local percentage=$2
  echo $(echo "$speed * $percentage" | bc | awk '{print int($1+0.5)}')
}

# Yüzdelik oranlar
PERCENTAGES="90 85 80"

for PERCENTAGE in $PERCENTAGES; do
  PERCENT=$(echo "$PERCENTAGE / 100" | bc -l)
  SQM_DOWNLOAD=$(calculate_sqm $DOWNLOAD_SPEED_KBPS $PERCENT)
  SQM_UPLOAD=$(calculate_sqm $UPLOAD_SPEED_KBPS $PERCENT)
  
  echo "Önerilen SQM için ayarlanacak Download Hızı ($PERCENTAGE%): $SQM_DOWNLOAD Kbps"
  echo "Önerilen SQM için ayarlanacak Upload Hızı ($PERCENTAGE%): $SQM_UPLOAD Kbps"
done
