#!/bin/bash

# Hata kontrolü: Kod girilmezse
if [ $# -ne 1 ]; then
  echo "Kullanım: $0 <kod>" >&2
  exit 1
fi

KOD="$1"
URL="https://user.goknet.com.tr/sistem/getTTAddressWebservice.php?kod=$KOD&datatype=checkAddress"
FILE="veriler.json"

# JSON verilerini indir
curl -s "$URL" > "$FILE"

# Hata kontrolü: İndirme başarısız olursa
if [ $? -ne 0 ]; then
  echo "Hata: JSON verileri indirilemedi." >&2
  exit 1
fi

# JSON verilerini işle ve tabloyu dosyaya kaydet
jq '.[] | [.IL, .ILCE, .BUCAK, .KOY, .MAHALLE, .CADDE, .SOKAK, .SITE, .APT, .NO, .DAIRE, .IC_KAPI_NO]' "$FILE" | column -t > adresler.txt

echo "Adres bilgileri 'adresler.txt' dosyasına kaydedildi."