#!/bin/sh

# Error Handling
set -e

# Log file
LOGFILE="/var/log/setup_script.log"
exec > >(tee -a ${LOGFILE}) 2>&1

# Variables
USER=$(whoami)
HOME_DIR=$(eval echo ~$USER)
ZSH_CUSTOM="${ZSH_CUSTOM:=$HOME_DIR/.oh-my-zsh/custom}"

# Ensure the script is run as the intended user
if [ "$USER" = "root" ]; then
  echo "Please do not run this script as root. Use your regular user account."
  exit 1
fi

# Function to handle errors
error_exit() {
  echo "$1" 1>&2
  exit 1
}

# Dependency check function
check_dependencies() {
  echo "Checking for required dependencies..."
  command -v doas >/dev/null 2>&1 || { echo "doas is required but it's not installed. Aborting." >&2; exit 1; }
  command -v flatpak >/dev/null 2>&1 || { echo "flatpak is required but it's not installed. Aborting." >&2; exit 1; }
}

# General package installation
install_general_packages() {
  echo "Installing general packages..."
  doas apk add py3-pip fastfetch android-tools rust npm git wget curl starship || error_exit "Failed to install general packages"
}

# Python setup
setup_python() {
  echo "Setting up Python..."
  pip3 install --break-system-packages -U pip yt-dlp setuptools wheel || error_exit "Failed to install Python packages"
}

# Git configuration
configure_git() {
  echo "Configuring Git..."
  git config --global user.email "root@localhost.localdomain" || error_exit "Failed to configure Git email"
  git config --global user.name "Root" || error_exit "Failed to configure Git username"
  git config --global credential.helper "cache --timeout=36000" || error_exit "Failed to configure Git credential helper"
}

# ZSH setup
setup_zsh() {
  echo "Setting up ZSH..."
  doas apk add zsh || error_exit "Failed to install ZSH"
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended || error_exit "Failed to install Oh My Zsh"
  git clone https://github.com/zsh-users/zsh-completions.git ${ZSH_CUSTOM}/plugins/zsh-completions || error_exit "Failed to clone zsh-completions"
  git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM}/plugins/zsh-syntax-highlighting || error_exit "Failed to clone zsh-syntax-highlighting"
  git clone https://github.com/zsh-users/zsh-autosuggestions.git ${ZSH_CUSTOM}/plugins/zsh-autosuggestions || error_exit "Failed to clone zsh-autosuggestions"
  rm -rf ~/.zshrc && wget -O ~/.zshrc https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc || error_exit "Failed to download .zshrc"
}

# Flatpak setup
setup_flatpak() {
  echo "Setting up Flatpak..."
  doas apk add flatpak || error_exit "Failed to install Flatpak"
  flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo || error_exit "Failed to add Flathub remote"
  flatpak remote-add --if-not-exists flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo || error_exit "Failed to add Flathub Beta remote"
  flatpak update && flatpak upgrade || error_exit "Failed to update Flatpak"
}

# Install Flatpak apps
install_flatpak_apps() {
  echo "Installing Flatpak apps..."
  flatpak install flathub net.mullvad.MullvadBrowser -y || error_exit "Failed to install Mullvad Browser"
  flatpak install flathub com.brave.Browser -y || error_exit "Failed to install Brave Browser"
  flatpak install flathub io.freetubeapp.FreeTube -y || error_exit "Failed to install FreeTube"
  flatpak install flathub io.github.mimbrero.WhatsAppDesktop -y || error_exit "Failed to install WhatsApp Desktop"
  flatpak install flathub com.mattjakeman.ExtensionManager -y || error_exit "Failed to install Extension Manager"
  flatpak install flathub com.github.ADBeveridge.Raider -y || error_exit "Failed to install Raider"
  flatpak install flathub org.onionshare.OnionShare -y || error_exit "Failed to install OnionShare"
  flatpak install flathub de.haeckerfelix.Fragments -y || error_exit "Failed to install Fragments"
}

# Remove unwanted packages
remove_unwanted_packages() {
  echo "Removing unwanted packages..."
  doas apk del firefox || error_exit "Failed to remove Firefox"
  doas apk del epiphany || error_exit "Failed to remove Epiphany"
}

# Update user directories
update_user_dirs() {
  echo "Updating user directories..."
  xdg-user-dirs-update || error_exit "Failed to update user directories"
}

# Main
main() {
  check_dependencies
  install_general_packages
  setup_python
  configure_git
  setup_zsh
  setup_flatpak
  install_flatpak_apps
  update_user_dirs
  remove_unwanted_packages
  echo "Setup complete."
}

main