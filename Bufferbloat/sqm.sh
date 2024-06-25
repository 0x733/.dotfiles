#!/bin/sh

# İnternet hız testi
echo "Hız testi yapılıyor..."
SPEEDTEST_OUTPUT=$(speedtest-go --nearest)

# Download ve Upload hızlarını çıkarma
DOWNLOAD_SPEED=$(echo "$SPEEDTEST_OUTPUT" | grep "Download" | awk '{print $2}')
UPLOAD_SPEED=$(echo "$SPEEDTEST_OUTPUT" | grep "Upload" | awk '{print $2}')

# Hızları Kbps cinsine çevirme (Speedtest-go sonucu Mbps cinsindendir)
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

# Ping testi
ping_test() {
  local target=$1
  echo "Ping testi: $target"
  ping -c 4 $target
}

# DNS testi
dns_test() {
  local target=$1
  echo "DNS testi: $target"
  nslookup $target
}

# Paket kaybı testi
packet_loss_test() {
  local target=$1
  echo "Paket kaybı testi (mtr): $target"
  sudo mtr -r -c 10 $target
}

# Testleri çalıştırma
run_tests() {
  local targets=$1
  for target in $targets; do
    ping_test $target
    dns_test $target
    packet_loss_test $target
  done
}

# Test hedefleri
DNS_SERVERS="8.8.8.8 1.1.1.1 9.9.9.9 208.67.222.222 8.8.4.4"
SEARCH_ENGINES="google.com bing.com duckduckgo.com yahoo.com baidu.com"
GAME_SERVERS="csgo.com leagueoflegends.com dota2.com overwatch.com pubg.com"

# DNS sunucuları test et
echo "DNS Sunucuları test ediliyor..."
run_tests "$DNS_SERVERS"

# Arama motorları test et
echo "Arama Motorları test ediliyor..."
run_tests "$SEARCH_ENGINES"

# Oyun sunucuları test et
echo "Oyun Sunucuları test ediliyor..."
run_tests "$GAME_SERVERS"

echo "Tüm testler tamamlandı."