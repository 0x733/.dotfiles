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

# Tam hızların %90'ını kullanarak SQM ayarlarını hesaplama
SQM_DOWNLOAD=$(echo "$DOWNLOAD_SPEED_KBPS * 0.9" | bc | awk '{print int($1+0.5)}')
SQM_UPLOAD=$(echo "$UPLOAD_SPEED_KBPS * 0.9" | bc | awk '{print int($1+0.5)}')

echo "Önerilen SQM için ayarlanacak Download Hızı: $SQM_DOWNLOAD Kbps"
echo "Önerilen SQM için ayarlanacak Upload Hızı: $SQM_UPLOAD Kbps"
