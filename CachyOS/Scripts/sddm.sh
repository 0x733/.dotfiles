#!/bin/bash

echo "SDDM Tema Kurulum Scripti başlatılıyor..."

# Root yetkilerinin kontrolü
if [[ $EUID -ne 0 ]]; then
   echo "Bu scriptin çalışması için root yetkilerine ihtiyacınız var. Lütfen sudo ile çalıştırın."
   exit 1
fi

# Bağımlılıkları kur (onay gerektirmeden)
echo "Gerekli bağımlılıklar kuruluyor..."
pacman --noconfirm -Syu qt6-svg qt6-declarative || {
    echo "Hata: Bağımlılıklar kurulamadı. Lütfen internet bağlantınızı kontrol edin ve tekrar deneyin."
    exit 1
}

# Temayı indir
echo "Tema indiriliyor..."
wget -P /usr/share/sddm/themes/ https://github.com/catppuccin/sddm/releases/download/v1.0.0/catppuccin-mocha.zip || {
    echo "Hata: Tema indirilemedi. Lütfen internet bağlantınızı kontrol edin ve tekrar deneyin."
    exit 1
}

# Temayı unzip et
echo "Tema açılıyor..."
unzip /usr/share/sddm/themes/catppuccin-mocha.zip -d /usr/share/sddm/themes/ || {
    echo "Hata: Tema açılamadı."
    exit 1
}

# Zip dosyasını sil
echo "Zip dosyası siliniyor..."
rm /usr/share/sddm/themes/catppuccin-mocha.zip

# Tema ayarını yap (Eğer [Theme] bölümü yoksa ekle)
if ! grep -q "^\[Theme\]" /etc/sddm.conf; then
    echo "[Theme]" | tee -a /etc/sddm.conf
fi
echo "Current=catppuccin-mocha" | tee -a /etc/sddm.conf

# SDDM hizmetini yeniden başlat
echo "SDDM yeniden başlatılıyor..."
systemctl restart sddm

echo "SDDM Tema Kurulum Scripti başarıyla tamamlandı!"

