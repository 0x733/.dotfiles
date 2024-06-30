install_flatpak_whatsapp() {
  echo "Flatpak ve WhatsApp Desktop kuruluyor..."
  sudo pacman -Sy --noconfirm flatpak
  flatpak install flathub io.github.mimbrero.WhatsAppDesktop -y
}
