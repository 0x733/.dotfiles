#!/bin/bash

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

shred_temp_files() {
    echo "Geçici dosyalar güvenli bir şekilde siliniyor..."
    sudo find /tmp -type f \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o -name "${uzantilar[2]}" -o -name "${uzantilar[3]}" -o -name "${uzantilar[4]}" -o -name "${uzantilar[5]}" -o -name "${uzantilar[6]}" -o -name "${uzantilar[7]}" -o -name "${uzantilar[8]}" \) -exec shred -u {} \;
    sudo find /var/tmp -type f \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o -name "${uzantilar[2]}" -o -name "${uzantilar[3]}" -o -name "${uzantilar[4]}" -o -name "${uzantilar[5]}" -o -name "${uzantilar[6]}" -o -name "${uzantilar[7]}" -o -name "${uzantilar[8]}" \) -exec shred -u {} \;
    echo "Geçici dosyalar güvenli bir şekilde silindi."
}

clear_zsh_history() {
    echo "zsh komut geçmişi siliniyor..."
    rm -f ~/.zsh_history
    touch ~/.zsh_history
    echo "zsh komut geçmişi silindi."
}

clean_package_cache() {
    echo "Paket önbelleği temizleniyor..."
    sudo pacman -Sc --noconfirm
    echo "Paket önbelleği temizlendi."
}

remove_orphans() {
    echo "Orphan paketler kaldırılıyor..."
    sudo pacman -Rns $(sudo pacman -Qdtq) --noconfirm
    echo "Orphan paketler kaldırıldı."
}

disk_cleanup() {
    echo "Disk temizliği yapılıyor..."
    sudo rm -rf /var/cache/pacman/pkg/*
    echo "Pacman paket önbelleği temizlendi."
    sudo find /var/log -type f \( -name "*.log" \) -exec rm -f {} \;
    echo "Log dosyaları temizlendi."
    sudo find / -type f \( -name "${uzantilar[0]}" -o -name "${uzantilar[1]}" -o -name "${uzantilar[2]}" -o -name "${uzantilar[3]}" -o -name "${uzantilar[4]}" -o -name "${uzantilar[5]}" -o -name "${uzantilar[6]}" -o -name "${uzantilar[7]}" -o -name "${uzantilar[8]}" \) -exec rm -f {} \;
    echo "Belirtilen uzantılara sahip dosyalar temizlendi."
}

clean_whatsapp_cache() {
    echo "WhatsApp Desktop cache'i temizleniyor..."
    rm -rf ~/.var/app/io.github.mimbrero.WhatsAppDesktop/cache/*
    echo "WhatsApp Desktop cache'i temizlendi."
}

clean_home_cache() {
    echo ".cache dizini temizleniyor..."
    rm -rf ~/.cache/*
    echo ".cache dizini temizlendi."
}

memory_optimization() {
    echo "Bellek optimizasyonu yapılıyor..."
    sudo sync
    sudo sysctl -w vm.drop_caches=3
    echo "Bellek optimizasyonu tamamlandı."
}

system_update() {
    echo "Sistem güncelleniyor..."
    sudo pacman -Syu --noconfirm
    echo "Sistem güncellendi."
}

# Tüm fonksiyonları çağırma
shred_temp_files
clear_zsh_history
clean_package_cache
remove_orphans
disk_cleanup
clean_whatsapp_cache
clean_home_cache
memory_optimization
system_update

echo "Tüm işlemler tamamlandı."

