#!/bin/bash

# Ublock Origin Eklentisi Kurulumu ve Yapılandırması

# Ublock Origin Eklenti URL'si (Stabil sürüm)
ublock_origin_url="https://github.com/gorhill/uBlock/releases/download/1.58.0/uBlock0_1.58.0.chromium.zip"

# Ublock Origin Config Dosyası URL
ublock_config_url="https://raw.githubusercontent.com/0x733/.dotfiles/main/Brave%20%26%20Mullvad/ublock.txt"

# Brave tarayıcı profil dizini
brave_profile_dir="$HOME/.config/BraveSoftware/Brave-Browser/Default/Extensions/ublock@raymondhill.net/uBlock0.chromium"

# Fonksiyonlar

# Ublock Origin Eklentisi Kurulumu
install_ublock_origin() {
    local extension_url=$1
    local config_url=$2
    local profile_dir=$3
    
    # Brave profil dizini kontrolü
    if [ ! -d "$(dirname "$profile_dir")" ]; then
        echo "Hata: Brave tarayıcı profili bulunamadı. Lütfen Brave tarayıcısını en az bir kez çalıştırın."
        return 1
    fi
    
    # Eklenti dosyasının indirilmesi ve kurulması
    echo "Ublock Origin eklentisi indiriliyor ve kuruluyor..."
    wget -O ublock.zip "$extension_url"
    if [ $? -ne 0 ]; then
        echo "Hata: Ublock Origin eklentisi indirilemedi."
        return 1
    fi
    
    unzip -qo ublock.zip -d ublock
    if [ $? -ne 0 ]; then
        echo "Hata: Ublock Origin eklentisi açılamadı."
        return 1
    fi
    
    mkdir -p "$(dirname "$profile_dir")"
    cp -r ublock/* "$profile_dir"
    
    # Konfigürasyon dosyasının yüklenmesi
    echo "Ublock Origin konfigürasyon dosyası yükleniyor..."
    wget -O "$profile_dir/config.txt" "$config_url"
    if [ $? -ne 0 ]; then
        echo "Hata: Ublock Origin konfigürasyon dosyası indirilemedi."
        return 1
    fi
    
    # Manifest dosyasının güncellenmesi
    local manifest_file="$profile_dir/manifest.json"
    if [ -f "$manifest_file" ]; then
        sed -i 's/"version":.*/"version": "1.0",/' "$manifest_file"
        echo "Ublock Origin manifest dosyası güncellendi."
    else
        echo "Hata: Manifest dosyası bulunamadı veya dizin yanlış."
        return 1
    fi
    
    echo "Ublock Origin eklentisi başarıyla kuruldu ve yapılandırıldı."
}

# Ublock Origin eklentisi kurulumu
echo "Ublock Origin eklentisi Brave tarayıcısına kuruluyor..."
install_ublock_origin "$ublock_origin_url" "$ublock_config_url" "$brave_profile_dir"

if [ $? -eq 0 ]; then
    echo "Ublock Origin eklentisi Brave tarayıcısına başarıyla kuruldu ve yapılandırıldı."
else
    echo "Ublock Origin eklentisi kurulurken bir hata oluştu."
fi