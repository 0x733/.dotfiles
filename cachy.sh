#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

LOGFILE="${HOME}/setup_script.log"
exec &>> "${LOGFILE}"

USER="${USER:-$(whoami)}"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/hypr"
DOTFILES_DIR="${HOME}/.dotfiles/.dots"

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') $*"
}

warn() {
  log "UYARI: $*" >&2
}

error_exit() {
  log "HATA: $*" >&2
  exit 1
}

show_progress() {
  local msg="$1"
  local total="$2"
  local current=0

  dialog --title "Kurulum" --gauge "$msg" 10 50 0

  while [ $current -lt $total ]; do
    ((current++))
    dialog --gauge "" 10 50 $((current * 100 / total))
    sleep 0.1
  done

  dialog --msgbox "İşlem tamamlandı." 5 30
}

update_system() {
  log "Sistem güncelleniyor ve paketler yükleniyor..."
  show_progress "Sistem güncelleniyor..." 1
  sudo pacman -Syu --noconfirm || error_exit "Sistem güncelleme başarısız"
}

configure_hyprland() {
  log "Hyprland yapılandırılıyor..."
  show_progress "Hyprland yapılandırılıyor..." 1
  mkdir -p "${CONFIG_DIR}"
  cp "${CONFIG_DIR}/hyprland.conf" "${CONFIG_DIR}/hyprland.conf.bak" || warn "hyprland.conf yedekleme başarısız"
  sed -i -e 's/^bind = CTRL, SPACE, exec, rofi -show combi.*/bind = CTRL, SPACE, exec, wofi/' \
          -e 's/kb_layout = us/kb_layout = tr/' \
          "${CONFIG_DIR}/hyprland.conf"
}
setup_chaotic_aur() {
  log "Chaotic AUR kuruluyor..."
  show_progress "Chaotic AUR kuruluyor..." 3
  sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com || error_exit "Chaotic AUR anahtarı alınamadı"
  sudo pacman-key --lsign-key 3056513887B78AEB || error_exit "Chaotic AUR anahtarı yerel olarak imzalanamadı"
  sudo pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst' || error_exit "Chaotic AUR paketleri kurulamadı"
  sudo cp /etc/pacman.conf /etc/pacman.conf.bak || error_exit "pacman.conf yedeklenemedi"
  echo -e "\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist" | sudo tee -a /etc/pacman.conf || error_exit "Chaotic AUR, pacman.conf'da yapılandırılamadı"
}

install_packages() {
  log "Ek paketler yükleniyor..."
  local packages=(
    "git"
    "wget"
    "curl"
    "xdg-user-dirs"
    "playerctl"
    "unzip"
    "zip"
    "p7zip"
    "unrar"
    "tar"
    "rsync"
    "qt5ct"
    "kvantum"
  )
  local total=${#packages[@]}

  show_progress "Ek paketler yükleniyor (pacman)..." $total

  for package in "${packages[@]}"; do
    sudo pacman -S --noconfirm "$package" || error_exit "Paket yükleme başarısız: $package"
  done

  log "AUR paketleri yükleniyor (paru)..."
  local aur_packages=(
    "qt5-styleplugins"
  )
  total=${#aur_packages[@]}

  show_progress "AUR paketleri yükleniyor (paru)..." $total

  for package in "${aur_packages[@]}"; do
    paru -S --noconfirm "$package" || error_exit "Paket yükleme başarısız: $package"
  done
}

install_pacman_apps() {
  log "Pacman paketleri yükleniyor..."
  local packages=(
    "brave-browser-bin"
    "mullvad-browser-bin"
    "whatsapp-for-linux"
    "onionshare"
    "vlc"
    "dolphin-emu"
    "yt-dlp"
    "starship"
    "waydroid"
  )
  local total=${#packages[@]}

  show_progress "Pacman paketleri yükleniyor..." $total

  for package in "${packages[@]}"; do
    sudo pacman -S --noconfirm "$package" || error_exit "Paket yükleme başarısız: $package"
  done
}
install_file_viewer() {
  log "Dosya görüntüleyici (pcmanfm) kuruluyor..."
  show_progress "Dosya görüntüleyici kuruluyor..." 1
  sudo pacman -Syu --noconfirm --needed pcmanfm || error_exit "pcmanfm kurulumu başarısız"
}

setup_kvantum_theme() {
  log "Kvantum teması ayarlanıyor..."
  show_progress "Kvantum teması ayarlanıyor..." 4

  qt5ct &  # Kvantum ayarlarını aç
  sleep 5  # Ayarların yüklenmesi için kısa bir süre bekle

  # Kvantum temasını ayarla (örneğin, kvantum-dark)
  kvantummanager --set kvantum-dark

  # Pencere dekorasyonunu Kvantum'a ayarla
  qt5ct --set-window-theme Kvantum
}

configure_git() {
  log "Git yapılandırılıyor..."
  show_progress "Git yapılandırılıyor..." 3

  git config --global user.email "root@localhost.localdomain" || error_exit "Git e-posta yapılandırması başarısız"
  git config --global user.name "Root" || error_exit "Git kullanıcı adı yapılandırması başarısız"
  git config --global credential.helper "cache --timeout=36000" || error_exit "Git credential helper yapılandırması başarısız"
}

setup_zsh() {
  log "ZSH kuruluyor..."
  show_progress "ZSH kuruluyor..." 4

  sudo pacman -Sy --noconfirm --needed zsh || error_exit "ZSH kurulumu başarısız"
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended || error_exit "Oh My Zsh kurulumu başarısız"
  git clone https://github.com/zsh-users/zsh-completions.git "${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions" || error_exit "zsh-completions klonlanamadı"
  git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting" || error_exit "zsh-syntax-highlighting klonlanamadı"
  git clone https://github.com/zsh-users/zsh-autosuggestions.git "${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions" || error_exit "zsh-autosuggestions klonlanamadı"
  rm -rf ~/.zshrc && wget -O ~/.zshrc https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc || error_exit ".zshrc indirilemedi"
}

update_user_dirs() {
  log "Kullanıcı dizinleri güncelleniyor..."
  show_progress "Kullanıcı dizinleri güncelleniyor..." 1
  xdg-user-dirs-update || error_exit "Kullanıcı dizinleri güncellenemedi"
}

setup_fonts() {
  log "Yazı tipleri kuruluyor..."
  show_progress "Yazı tipleri kuruluyor..." 3

  cp "$DOTFILES_DIR/.fonts.conf" "$HOME/" || error_exit ".fonts.conf kopyalanamadı"
  cp -r "$DOTFILES_DIR/.fonts" "$HOME/" || error_exit ".fonts dizini kopyalanamadı"
  cp -r "$DOTFILES_DIR/.config/fontconfig" "$HOME/.config/" || error_exit "fontconfig kopyalanamadı"
}

install_video_dependencies() {
  log "Video oynatma bağımlılıkları kuruluyor..."
  show_progress "Video oynatma bağımlılıkları kuruluyor..." 1

  sudo pacman -Sy --noconfirm gstreamer gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav || error_exit "Video oynatma bağımlılıkları kurulamadı"
}

main() {
  update_system
  configure_hyprland
  setup_chaotic_aur
  install_packages
  configure_git
  setup_zsh
  install_pacman_apps
  update_user_dirs
  setup_fonts
  install_video_dependencies
  install_file_viewer
  setup_kvantum_theme
  log "Kurulum tamamlandı. Sistem yeniden başlatılıyor..."
  reboot
}

# Check if script is run with sudo
if [[ $(id -u) -eq 0 ]]; then
  log "Lütfen bu komut dosyasını root olarak çalıştırmayın. Normal kullanıcı hesabınızı kullanın."
  exit 1
fi

main
