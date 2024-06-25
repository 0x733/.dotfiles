#!/bin/bash

dizinler=(
    "$HOME/.cache"
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
        if [[ "$dizin" == "/var/log" || "$dizin" == "/var/tmp" ]]; then
            if [ -n "$gun" ]; then
                sudo find "$dizin" -type f -mtime +"$gun" \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o ... \) -exec shred -uz {} +
            else
                sudo find "$dizin" -type f \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o ... \) -exec shred -uz {} +
            fi
        else
            if [ -n "$gun" ]; then
                find "$dizin" -type f -mtime +"$gun" \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o ... \) -exec shred -uz {} +
            else
                find "$dizin" -type f \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o ... \) -exec shred -uz {} +
            fi
        fi
    fi
}

# Geçmişi temizle (root gerektirmez)
history -c
shred -uz ~/.zsh_history
shred -uz ~/.bash_history

# Pacman işlemleri (sudo gerektirir)
sudo pacman -Sc  # Önbelleği senkronize et
sudo pacman -Qdt # Yetim paketleri listele
read -p "Yetim paketler silinsin mi? (e/h) " cevap
if [ "$cevap" = "e" ]; then
    sudo pacman -Rns $(pacman -Qdtq) # Yetim paketleri kaldır
fi

# Kullanıcıdan temizlenecek dizinleri seçmesini iste
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

# Boş dizinleri sil
for dizin in "${dizinler[@]}"; do
    if [ -d "$dizin" ]; then 
        if [[ "$dizin" == "/var/log" || "$dizin" == "/var/tmp" ]]; then
            sudo find "$dizin" -mindepth 1 -type d -empty -delete 
        else
            find "$dizin" -mindepth 1 -type d -empty -delete 
        fi
    fi
done

echo "Temizleme işlemi tamamlandı!"
