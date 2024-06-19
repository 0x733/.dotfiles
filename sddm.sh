#!/bin/bash

# CachyOS SDDM Tema Paketi Kurulum Scripti

# Paket adı
pkg_name="cachyos-themes-sddm"

# Paketi kur
echo "CachyOS SDDM teması kuruluyor..."
sudo pacman -Sy --noconfirm $pkg_name

# Temayı etkinleştir
echo "SDDM tema ayarları güncelleniyor..."
sudo sed -i 's/^Current=.*$/Current='$pkg_name'/' /etc/sddm.conf

# SDDM'yi yeniden başlat
echo "SDDM yeniden başlatılıyor..."
sudo systemctl restart sddm

echo "CachyOS SDDM tema başarıyla kuruldu ve etkinleştirildi."