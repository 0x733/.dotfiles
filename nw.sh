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
jq -r 'keys[] as $k | .[$k].flexList.flexList[] | [.name, .value] | @tsv' "$FILE" > adresler.txt

# Boş satırları ve hata içeren satırları kaldır
sed -i '/^$/d' adresler.txt
sed -i '/hataKod/d' adresler.txt
sed -i '/hataMesaj/d' adresler.txt

echo "Adres bilgileri 'adresler.txt' dosyasına kaydedildi."
