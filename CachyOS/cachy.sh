#!/bin/bash

set -euo pipefail

USER="${USER:-$(whoami)}"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/hypr"
DOTFILES_DIR="${HOME}/.dotfiles/.dots"

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') $*"
}

update_system() {
  echo "Sistem güncelleniyor ve paketler yükleniyor..."
  sudo pacman -Syu --noconfirm
}

configure_hyprland() {
  echo "Hyprland yapılandırılıyor..."
  mkdir -p "${CONFIG_DIR}"
  cp "${CONFIG_DIR}/hyprland.conf" "${CONFIG_DIR}/hyprland.conf.bak"
  sed -i -e 's/^bind = CTRL, SPACE, exec, rofi -show combi.*/bind = CTRL, SPACE, exec, wofi/' \
         -e 's/kb_layout = us/kb_layout = tr/' \
         "${CONFIG_DIR}/hyprland.conf"
}

setup_chaotic_aur() {
  echo "Chaotic AUR kuruluyor..."
  sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
  sudo pacman-key --lsign-key 3056513887B78AEB
  sudo pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' \
                            'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'
  sudo cp /etc/pacman.conf /etc/pacman.conf.bak
  echo -e "\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist" | sudo tee -a /etc/pacman.conf
}

setup_black_arch() {
  echo "Black Arch kuruluyor..."
  curl -O https://blackarch.org/strap.sh
  echo "5f3d815e424213e9b6b278a859f6d47426f0b3b0 strap.sh" | sha1sum -c -
  chmod +x strap.sh
  sudo ./strap.sh
  rm strap.sh
}

install_packages() {
  echo "Ek paketler yükleniyor..."
  local packages=(
    "git" "wget" "curl" "xdg-user-dirs" "playerctl" "unzip" "zip"
    "p7zip" "unrar" "tar" "rsync" "qt5ct" "kvantum" "gvfs" "gvfs-smb" "gvfs-mtp"
    "gvfs-afc" "gvfs-goa" "gvfs-google" "gvfs-gphoto2" "gvfs-nfs" "gvfs-afc"
  )
  sudo pacman -Sy --noconfirm "${packages[@]}"

  echo "AUR paketleri yükleniyor..."
  local aur_packages=("qt5-styleplugins")
  paru -Sy --noconfirm "${aur_packages[@]}"
}

install_pacman_apps() {
  echo "Pacman paketleri yükleniyor..."
  local packages=(
    "brave-bin" "mullvad-browser-bin" "onionshare"
    "vlc" "dolphin-emu" "yt-dlp" "starship" "waydroid" 
    "chatgpt-desktop-bin"
  )
  sudo pacman -Sy --noconfirm "${packages[@]}"
}

install_file_viewer() {
  echo "Dosya görüntüleyici (pcmanfm) kuruluyor..."
  sudo pacman -Sy --noconfirm --needed pcmanfm
}

setup_kvantum_theme() {
  echo "Kvantum teması ayarlanıyor..."
  qt5ct & 
  sleep 5
  kvantummanager --set kvantum-dark
  qt5ct --set-window-theme Kvantum
}

configure_git() {
  echo "Git yapılandırılıyor..."
  git config --global user.email "root@localhost.localdomain"
  git config --global user.name "Root"
  git config --global credential.helper store
}

setup_zsh() {
  echo "ZSH kuruluyor..."
  sudo pacman -Sy --noconfirm --needed zsh
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

  # ZSH_CUSTOM dizinini tanımlayın
  ZSH_CUSTOM=${ZSH_CUSTOM:-~/.oh-my-zsh/custom}

  # Eklenti dizinlerinin var olduğundan emin olun
  mkdir -p $ZSH_CUSTOM/plugins/zsh-completions
  mkdir -p $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
  mkdir -p $ZSH_CUSTOM/plugins/zsh-autosuggestions

  # Eklentileri klonlayın
  git clone --depth 1 https://github.com/zsh-users/zsh-completions.git $ZSH_CUSTOM/plugins/zsh-completions
  git clone --depth 1 https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
  git clone --depth 1 https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions

  # .zshrc yapılandırma dosyasını indirin
  rm -rf ~/.zshrc && wget -q --show-progress --progress=bar:force:noscroll -O ~/.zshrc https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc

  # ZSH kabuğunu varsayılan kabuk olarak ayarlayın
  chsh -s /bin/zsh
}

install_flatpak_whatsapp() {
  echo "Flatpak ve WhatsApp Desktop kuruluyor..."
  sudo pacman -Sy --noconfirm flatpak
  flatpak install flathub io.github.mimbrero.WhatsAppDesktop -y
}

update_user_dirs() {
  echo "Kullanıcı dizinleri güncelleniyor..."
  xdg-user-dirs-update
}

setup_fonts() {
  echo "Yazı tipleri kuruluyor..."
  local font_packages=("noto-fonts" "noto-fonts-cjk" "noto-fonts-emoji" "noto-fonts-extra")
  sudo pacman -Sy --noconfirm "${font_packages[@]}"
  cp "$DOTFILES_DIR/.fonts.conf" "$HOME/"
  cp -r "$DOTFILES_DIR/.fonts" "$HOME/"
  cp -r "$DOTFILES_DIR/.config/fontconfig" "$HOME/.config/"
}

install_video_dependencies() {
  echo "Video oynatma bağımlılıkları kuruluyor..."
  sudo pacman -Sy --noconfirm gstreamer gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
}

main() {
  update_system
  configure_hyprland
  setup_chaotic_aur
  setup_black_arch
  install_packages
  install_pacman_apps
  install_file_viewer
  setup_kvantum_theme
  configure_git
  setup_zsh
  install_flatpak_whatsapp
  update_user_dirs
  setup_fonts
  install_video_dependencies
  echo "Kurulum tamamlandı. Sistem yeniden başlatılıyor..."
  sudo reboot
}

if [[ $(id -u) -eq 0 ]]; then
  echo "Lütfen bu komut dosyasını root olarak çalıştırmayın. Normal kullanıcı hesabınızı kullanın."
  exit 1
fi

main

echo "Script başarıyla çalıştı. İşlem tamamlandı."