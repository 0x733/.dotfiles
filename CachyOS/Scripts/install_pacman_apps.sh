echo "Pacman paketleri yükleniyor..."
  local packages=(
    "brave-bin" "librewolf" "onionshare"
    "vlc" "dolphin-emu" "yt-dlp" "starship" "waydroid" 
    "chatgpt-desktop-bin" "ferdium-bin" "rustdesk" "visual-studio-code-bin"
  )
  sudo pacman -Sy --noconfirm "${packages[@]}"
