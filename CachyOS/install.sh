#!/bin/bash

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Include each module from .dotfiles/CachyOS/Scripts directory
source "$SCRIPT_DIR/update_system.sh"
source "$SCRIPT_DIR/configure_hyprland.sh"
source "$SCRIPT_DIR/setup_chaotic_aur.sh"
source "$SCRIPT_DIR/setup_black_arch.sh"
source "$SCRIPT_DIR/install_packages.sh"
source "$SCRIPT_DIR/install_pacman_apps.sh"
source "$SCRIPT_DIR/install_file_viewer.sh"
source "$SCRIPT_DIR/setup_kvantum_theme.sh"
source "$SCRIPT_DIR/configure_git.sh"
source "$SCRIPT_DIR/setup_zsh.sh"
source "$SCRIPT_DIR/install_flatpak_whatsapp.sh"
source "$SCRIPT_DIR/update_user_dirs.sh"
source "$SCRIPT_DIR/setup_fonts.sh"
source "$SCRIPT_DIR/install_video_dependencies.sh"
source "$SCRIPT_DIR/sddm.sh"

# Main function
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
  configure_sddm 
  echo "Kurulum tamamlandı. Sistem yeniden başlatılıyor..."
  sudo reboot
}

# Check if running as root
if [[ $(id -u) -eq 0 ]]; then
  echo "Lütfen bu komut dosyasını root olarak çalıştırmayın. Normal kullanıcı hesabınızı kullanın."
  exit 1
fi

# Run main function
main

echo "Script başarıyla çalıştı. İşlem tamamlandı."

