#!/bin/bash

# Ublock Origin Eklentisi Kurulumu ve Yapılandırması

# Ublock Origin Eklenti URL'si (Stabil sürüm)
ublock_origin_url="https://github.com/gorhill/uBlock/releases/latest/download/uBlock0.chromium.zip"

# Ublock Origin Config Dosyası URL
ublock_config_url="https://raw.githubusercontent.com/0x733/.dotfiles/main/Brave%20%26%20Mullvad/ublock.txt"

# Brave tarayıcı profil dizini
brave_profile_dir="/opt/brave-bin/resources/brave_extension"

# Ublock Origin Eklentisi için fonksiyon
install_ublock_origin() {
    local profile_dir=$1
    local extension_url=$2
    
    # Eğer profile dizini mevcut değilse çıkış yap
    if [ ! -d "$profile_dir" ]; then
        echo "Hata: $profile_dir dizini bulunamadı!"
        return 1
    fi
    
    # Eklenti dosyasının indirilmesi ve kurulması
    echo "Ublock Origin eklentisi indiriliyor ve kuruluyor..."
    sudo -u root wget -O ublock.zip "$extension_url"
    sudo -u root unzip -qo ublock.zip -d ublock
    sudo -u root mkdir -p "$profile_dir/ublock@raymondhill.net"
    sudo -u root cp -r ublock/* "$profile_dir/ublock@raymondhill.net"
    
    # Konfigürasyon dosyasının yüklenmesi
    echo "Ublock Origin konfigürasyon dosyası yükleniyor..."
    sudo -u root wget -O "$profile_dir/ublock@raymondhill.net/config.txt" "$ublock_config_url"
    
    # Profil dizinindeki manifest dosyasının güncellenmesi
    sudo -u root sed -i 's/"version":.*/"version": "1.0",/' "$profile_dir/ublock@raymondhill.net/manifest.json"
    
    echo "Ublock Origin eklentisi başarıyla kuruldu ve yapılandırıldı."
}

# Brave tarayıcısı için Ublock Origin eklentisi kurulumu
echo "Brave tarayıcısı için Ublock Origin eklentisi kuruluyor..."
install_ublock_origin "$brave_profile_dir" "$ublock_origin_url"

echo "Ublock Origin eklentisi Brave tarayıcısına başarıyla kuruldu ve yapılandırıldı."