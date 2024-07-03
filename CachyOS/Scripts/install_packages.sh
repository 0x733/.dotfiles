install_packages() {
  echo "Ek paketler yükleniyor..."
  local packages=(
    "git" "wget" "curl" "xdg-user-dirs" "playerctl" "unzip" "zip"
    "p7zip" "unrar" "tar" "rsync" "qt5ct" "kvantum" "gvfs" "gvfs-smb" "gvfs-mtp"
    "gvfs-afc" "gvfs-goa" "gvfs-google" "gvfs-gphoto2" "gvfs-nfs" "gvfs-afc"
  )
  sudo pacman -Sy --noconfirm "${packages[@]}"
}
