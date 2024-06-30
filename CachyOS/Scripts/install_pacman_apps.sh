install_pacman_apps() {
  echo "Pacman paketleri yükleniyor..."
  local packages=(
    "brave-bin" "mullvad-browser-bin" "onionshare"
    "vlc" "dolphin-emu" "yt-dlp" "starship" "waydroid" 
    "chatgpt-desktop-bin"
  )
  sudo pacman -Sy --noconfirm "${packages[@]}"
}
