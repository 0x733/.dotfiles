install_pacman_apps() {
  echo "Pacman paketleri yükleniyor..."
  local packages=(
    "brave-bin" "librewolf" "onionshare"
    "vlc" "dolphin-emu" "yt-dlp" "starship" "waydroid" 
    "chatgpt-desktop-bin" "ferdium-bin" "rustdesk"
  )
  sudo pacman -Sy --noconfirm "${packages[@]}"
}
