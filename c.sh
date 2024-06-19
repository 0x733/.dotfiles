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
)

temizle_dizin() {
    local dizin="$1"
    if [ -d "$dizin" ]; then
        echo "Temizleniyor: $dizin"
        if [ ${#uzantilar[@]} -gt 0 ]; then
            find "$dizin" -type f \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o -name "${uzantilar[2]}" -o -name "${uzantilar[3]}" -o -name "${uzantilar[4]}" \) -exec shred -uzn {} +
        else
            find "$dizin" -type f -exec shred -uzn {} +
        fi
    fi
}

echo "Komut geçmişi temizleniyor (Zsh)..."
history -c
shred -uzn ~/.zsh_history

for dizin in "${dizinler[@]}"; do
    temizle_dizin "$dizin"
done