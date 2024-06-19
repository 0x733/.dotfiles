#!/bin/bash

# Hata ayıklama ve güvenli kullanım için seçenekleri ayarla
set -euo pipefail

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') $*"
}

# Sistem güncelleme ve bağımlılıkların kurulumu
install_dependencies() {
  echo "Gerekli bağımlılıklar yükleniyor..."
  sudo pacman -Sy --noconfirm qt6-svg qt6-declarative
}

# Geçici dosyaları temizleme fonksiyonu
cleanup() {
  echo "Geçici dosyalar temizleniyor..."
  rm -rf /tmp/catppuccin-mocha*
}

# SDDM teması indirme ve kurulum
install_sddm_theme() {
  echo "SDDM teması indiriliyor ve kuruluyor..."
  wget -q --show-progress --progress=bar:force:noscroll -O /tmp/catppuccin-mocha.zip https://github.com/catppuccin/sddm/releases/download/v1.0.0/catppuccin-mocha.zip
  unzip -q /tmp/catppuccin-mocha.zip -d /tmp
  sudo mv /tmp/catppuccin-mocha /usr/share/sddm/themes/
}

# SDDM yapılandırma dosyasına tema ekleme
configure_sddm() {
  echo "SDDM yapılandırması güncelleniyor..."
  sudo mkdir -p /etc
  if grep -q "^\[Theme\]" /etc/sddm.conf; then
    sudo sed -i '/^\[Theme\]/!b;n;c\Current=catppuccin-mocha' /etc/sddm.conf
  else
    echo -e "\n[Theme]\nCurrent=catppuccin-mocha" | sudo tee -a /etc/sddm.conf
  fi
}

# Main fonksiyonu
main() {
  install_dependencies
  install_sddm_theme
  configure_sddm
  echo "SDDM teması kurulumu ve yapılandırması tamamlandı."
}

# Scripti root olarak çalıştırmamak için kontrol
if [[ $(id -u) -eq 0 ]]; then
  echo "Lütfen bu komut dosyasını root olarak çalıştırmayın. Normal kullanıcı hesabınızı kullanın."
  exit 1
fi

# Geçici dosyaları temizlemek için trap ayarı
trap cleanup EXIT

main