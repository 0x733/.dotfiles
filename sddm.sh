#!/bin/bash

# SDDM tema yapılandırması için gerekli bağımlılıkları yükle
sudo pacman -Syu --noconfirm qt6-svg qt6-declarative

# İndirilecek dosya ve dizinleri tanımla
tema_zip="catppuccin-mocha.zip"
tema_klasor="/usr/share/sddm/themes/"
sddm_conf="/etc/sddm.conf"

# Temayı indir
if [ ! -f "$tema_zip" ]; then
    wget https://github.com/catppuccin/sddm/releases/download/v1.0.0/catppuccin-mocha.zip
fi

# İndirilen zip dosyasını /usr/share/sddm/themes/ dizinine çıkart
sudo unzip -o "$tema_zip" -d "$tema_klasor"

# sddm.conf dosyasını düzenle
if ! grep -q "\[Theme\]" "$sddm_conf"; then
    sudo bash -c 'echo -e "\n[Theme]\nCurrent=catppuccin-mocha" >> "$sddm_conf"'
else
    sudo sed -i '/\[Theme\]/a Current=catppuccin-mocha' "$sddm_conf"
fi