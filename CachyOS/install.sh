#!/bin/bash

# Script directory
SCRIPT_DIR="$HOME/.dotfiles/CachyOS/Scripts"

# Include each module from .dotfiles/CachyOS/Scripts directory if it exists
for script in update_system configure_hyprland setup_chaotic_aur setup_black_arch install_packages install_pacman_apps install_file_viewer configure_git setup_zsh update_user_dirs setup_fonts install_video_dependencies sddm; do
  if [[ -f "$SCRIPT_DIR/$script.sh" ]]; then
    source "$SCRIPT_DIR/$script.sh"
  else
    echo "ERROR: Script not found: $SCRIPT_DIR/$script.sh" >&2
    exit 1
  fi
done

# Main function
main() {
  update_system
  configure_hyprland
  setup_chaotic_aur
  setup_black_arch
  install_packages
  install_pacman_apps
  install_file_viewer
  configure_git
  setup_zsh
  install_flatpak_whatsapp
  update_user_dirs
  setup_fonts
  install_video_dependencies
  configure_sddm 
  echo "Kurulum tamamlandı. Sistem yeniden başlatılıyor..."
  sudo reboot
}

# Check if running as root
if [[ $(id -u) -eq 0 ]]; then
  echo "Lütfen bu komut dosyasını root olarak çalıştırmayın. Normal kullanıcı hesabınızı kullanın." >&2
  exit 1
fi

# Run main function
main