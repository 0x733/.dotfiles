#!/bin/bash

dizinler=(
  "$HOME/.cache"
  "$HOME/.thumbnails"
  "/tmp"
  "/var/tmp"
  "/var/log"
)

uzantilar=(
  "*.tmp"
  "*.bak"
  "*.log"
  "*.old"
  "*.swp"
  "*.cache"
  "*.crash"
  "*.gz"
  "*.xz"
)

temizle_dizin() {
  dizin="$1"
  gun="$2"

  if [ -d "$dizin" ]; then
    if [ -n "$gun" ]; then
      find "$dizin" -type f -mtime +"$gun" \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o ... \) -exec shred -uzn {} +
    else
      find "$dizin" -type f \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o ... \) -exec shred -uzn {} +
    fi
  fi
}

history -c
shred -uzn ~/.zsh_history
shred -uzn ~/.bash_history

sudo pacman -Sc
sudo pacman -Qdt
read -p "Yetim paketler silinsin mi? (e/h) " cevap
if [ "$cevap" = "e" ]; then
  sudo pacman -Rns $(pacman -Qdtq)
fi

read -p "Tüm dizinleri temizlemek istiyor musunuz? (e/h) " cevap
if [ "$cevap" = "e" ]; then
  for dizin in "${dizinler[@]}"; do
    temizle_dizin "$dizin"
  done
else
  read -p "Hangi dizinleri temizlemek istersiniz? (Virgülle ayırarak girin) " secilen_dizinler
  for dizin in ${secilen_dizinler//,/ }; do
    temizle_dizin "$dizin"
  done
fi

find "${dizinler[@]}" -type d -empty -delete

echo "Temizleme işlemi tamamlandı!"