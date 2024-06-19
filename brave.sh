#!/bin/bash

# Ublock Origin Eklentisi Kurulumu ve Yapılandırması

# Ublock Origin Eklenti URL'si (Stabil sürüm)
ublock_origin_url="https://github.com/gorhill/uBlock/releases/latest/download/uBlock0.chromium.zip"

# Ublock Origin Config Dosyası URL
ublock_config_url="https://raw.githubusercontent.com/0x733/.dotfiles/main/Brave%20%26%20Mullvad/ublock.txt"

# Fonksiyonlar

# Ublock Origin Eklentisi Kurulumu
install_ublock_origin() {
    local extension_url=$1
    local config_url=$2
    local profile_dir="$HOME/.config/BraveSoftware/Brave-Browser/Default/Extensions/ublock@raymondhill.net"
    
    # Brave profil dizini kontrolü
    if [ ! -d "$HOME/.config/BraveSoftware/Brave-Browser/Default/Extensions" ]; then
        echo "Hata: Brave tarayıcı profili bulunamadı. Lütfen Brave tarayıcısını en az bir kez çalıştırın."
        return 1
    fi
    
    # Eklenti dosyasının indirilmesi ve kurulması
    echo "Ublock Origin eklentisi indiriliyor ve kuruluyor..."
    wget -O ublock.zip "$extension_url"
    unzip -qo ublock.zip -d ublock
    mkdir -p "$profile_dir"
    cp -r ublock/* "$profile_dir"
    
    # Konfigürasyon dosyasının yüklenmesi
    echo "Ublock Origin konfigürasyon dosyası yükleniyor..."
    wget -O "$profile_dir/config.txt" "$config_url"
    
    # Manifest dosyasının güncellenmesi
    sed -i 's/"version":.*/"version": "1.0",/' "$profile_dir/manifest.json"
    
    echo "Ublock Origin eklentisi başarıyla kuruldu ve yapılandırıldı."
}

# Ublock Origin eklentisi kurulumu
echo "Ublock Origin eklentisi Brave tarayıcısına kuruluyor..."
install_ublock_origin "$ublock_origin_url" "$ublock_config_url"

echo "Ublock Origin eklentisi Brave tarayıcısına başarıyla kuruldu ve yapılandırıldı."