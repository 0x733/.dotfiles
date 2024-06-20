#!/bin/bash

# Temizlenecek dizinler
dizinler=(
    "$HOME/.cache"
    "$HOME/.thumbnails"
    "/tmp"
    "/var/tmp"
    "/var/log"
)

# Silinecek dosya uzantıları
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

# Fonksiyon: Belirtilen dizini temizler
temizle_dizin() {
    local dizin="$1"
    local gun="$2" # Kaç günden eski dosyaları sileceğini belirtir (isteğe bağlı)

    if [ -d "$dizin" ]; then
        echo "Temizleniyor: $dizin"

        # Dosya yaşına göre silme (isteğe bağlı)
        if [ -n "$gun" ]; then
            find "$dizin" -type f -mtime +"$gun" \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o ... \) -exec shred -uzn {} +
        else
            find "$dizin" -type f \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o ... \) -exec shred -uzn {} +
        fi
    else
        echo "Hata: $dizin bulunamadı."
    fi
}

# Komut geçmişini temizle (Zsh, Bash ve diğerleri için)
echo "Komut geçmişi temizleniyor..."
history -c
shred -uzn ~/.zsh_history
shred -uzn ~/.bash_history

# İnteraktif mod (isteğe bağlı)
echo "Tüm dizinleri temizlemek istiyor musunuz? (e/h)"
read cevap

if [ "$cevap" = "e" ]; then
    for dizin in "${dizinler[@]}"; do
        temizle_dizin "$dizin"
    done
else
    echo "Hangi dizinleri temizlemek istersiniz? (Virgülle ayırarak girin)"
    read secilen_dizinler
    for dizin in ${secilen_dizinler//,/ }; do
        temizle_dizin "$dizin"
    done
fi

# Boş dizinleri sil (isteğe bağlı)
echo "Boş dizinler siliniyor..."
find "${dizinler[@]}" -type d -empty -delete

echo "Temizleme işlemi tamamlandı!"