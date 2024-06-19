#!/bin/bash

set -euo pipefail

remove_chaotic_aur() {
  echo "Chaotic AUR kaldırılıyor..."
  sudo pacman -Rns --noconfirm chaotic-keyring
  sudo sed -i '/\[chaotic-aur\]/,+1 d' /etc/pacman.conf
}

remove_chaotic_aur

echo "Chaotic AUR başarıyla kaldırıldı."