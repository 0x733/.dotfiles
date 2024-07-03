install_pacman_apps() {
  echo "Pacman paketleri yükleniyor..."
  local packages=(
    "brave-bin" "mullvad-browser-bin" "onionshare"
    "vlc" "dolphin-emu" "yt-dlp" "starship" "waydroid" 
    "chatgpt-desktop-bin" "ferdium-bin" "python-pipx"
  )
  sudo pacman -Sy --noconfirm "${packages[@]}"
}
