#!/bin/sh

# Error Handling
set -e

# Log file
LOGFILE="/var/log/setup_script.log"
exec > >(tee -a ${LOGFILE}) 2>&1

# Variables
USER=$(whoami)
CONFIG_DIR="/home/$USER/.config/hypr"
DOTFILES_DIR="/home/$USER/.dotfiles/.dots"

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

# Update system and install packages
update_system() {
  echo "Updating system and installing packages..."
  sudo pacman -Syu --noconfirm || error_exit "System update failed"
}

# Configure Rofi and Keyboard
configure_hyprland() {
  echo "Configuring Hyprland..."
  sed -i 's/^bind = CTRL, SPACE, exec, rofi -show combi -modi window,run,emoji,combi -combi-modi window,run,emoji/#&/; s/^#bind = CTRL, SPACE, exec, wofi/bind = CTRL, SPACE, exec, wofi/' $CONFIG_DIR/hyprland.conf || error_exit "Failed to configure Rofi"
  sed -i 's/kb_layout = us/kb_layout = tr/' $CONFIG_DIR/hyprland.conf || error_exit "Failed to configure keyboard layout"
}

# Setup Chaotic AUR
setup_chaotic_aur() {
  echo "Setting up Chaotic AUR..."
  sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com || error_exit "Failed to receive Chaotic AUR key"
  sudo pacman-key --lsign-key 3056513887B78AEB || error_exit "Failed to locally sign Chaotic AUR key"
  sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' || error_exit "Failed to install Chaotic keyring"
  sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst' || error_exit "Failed to install Chaotic mirrorlist"
  sudo cp /etc/pacman.conf /etc/pacman.conf.bak || error_exit "Failed to backup pacman.conf"
  echo -e "\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist" | sudo tee -a /etc/pacman.conf || error_exit "Failed to configure Chaotic AUR in pacman.conf"
}

# Install additional packages
install_packages() {
  echo "Installing additional packages..."
  sudo pacman -Sy --noconfirm --needed python-pip android-tools rust npm git wget curl starship waydroid || error_exit "Failed to install packages"
}

# Setup Python
setup_python() {
  echo "Setting up Python..."
  pip3 install --break-system-packages -U pip yt-dlp || error_exit "Failed to install Python packages"
}

# Configure Git
configure_git() {
  echo "Configuring Git..."
  git config --global user.email "root@localhost.localdomain" || error_exit "Failed to configure Git email"
  git config --global user.name "Root" || error_exit "Failed to configure Git username"
  git config --global credential.helper "cache --timeout=36000" || error_exit "Failed to configure Git credential helper"
}

# Setup ZSH
setup_zsh() {
  echo "Setting up ZSH..."
  sudo pacman -Sy --noconfirm --needed zsh || error_exit "Failed to install ZSH"
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended || error_exit "Failed to install Oh My Zsh"
  git clone https://github.com/zsh-users/zsh-completions.git ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions || error_exit "Failed to clone zsh-completions"
  git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting || error_exit "Failed to clone zsh-syntax-highlighting"
  git clone https://github.com/zsh-users/zsh-autosuggestions.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions || error_exit "Failed to clone zsh-autosuggestions"
  rm -rf ~/.zshrc && wget -O ~/.zshrc https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc || error_exit "Failed to download .zshrc"
}

# Setup Flatpak
setup_flatpak() {
  echo "Setting up Flatpak..."
  sudo pacman -Sy --noconfirm --needed flatpak || error_exit "Failed to install Flatpak"
  flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo || error_exit "Failed to add Flathub remote"
  flatpak remote-add --if-not-exists flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo || error_exit "Failed to add Flathub Beta remote"
  flatpak update && flatpak upgrade || error_exit "Failed to update Flatpak"
}

# Install Flatpak apps
install_flatpak_apps() {
  echo "Installing Flatpak apps..."
  flatpak install flathub net.mullvad.MullvadBrowser -y || error_exit "Failed to install Mullvad Browser"
  flatpak install flathub com.brave.Browser -y || error_exit "Failed to install Brave Browser"
  flatpak install flathub io.github.mimbrero.WhatsAppDesktop -y || error_exit "Failed to install WhatsApp Desktop"
  flatpak install flathub org.onionshare.OnionShare -y || error_exit "Failed to install OnionShare"
  flatpak install flathub de.haeckerfelix.Fragments -y || error_exit "Failed to install Fragments"
  flatpak install flathub org.videolan.VLC -y || error_exit "Failed to install VLC"
  flatpak install flathub io.frama.tractor.carburetor -y || error_exit "Failed to install Carburetor"
  flatpak install flathub org.kde.dolphin -y || error_exit "Failed to install Dolphin"
  flatpak install flathub org.kde.ark -y || error_exit "Failed to install Ark"
  flatpak install flathub org.DolphinEmu.dolphin-emu -y || error_exit "Failed to install Dolphin Emulator"
}

# Update user directories
update_user_dirs() {
  echo "Updating user directories..."
  xdg-user-dirs-update || error_exit "Failed to update user directories"
}

# Setup Fonts
setup_fonts() {
  echo "Setting up fonts..."
  cp $DOTFILES_DIR/.fonts.conf /home/$USER/ || error_exit "Failed to copy .fonts.conf"
  cp -r $DOTFILES_DIR/.fonts /home/$USER/ || error_exit "Failed to copy .fonts directory"
  cp -r $DOTFILES_DIR/.config/fontconfig ~/.config/ || error_exit "Failed to copy fontconfig"
}

# Video Playback Dependencies (Example for GStreamer)
install_video_dependencies() {
  echo "Installing video playback dependencies..."
  sudo pacman -Sy --noconfirm gstreamer gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav || error_exit "Failed to install video playback dependencies"
}

# Main
main() {
  update_system
  configure_hyprland
  setup_chaotic_aur
  install_packages
  setup_python
  configure_git
  setup_zsh
  setup_flatpak
  install_flatpak_apps
  update_user_dirs
  setup_fonts
  install_video_dependencies
  echo "Setup complete. Rebooting system..."
  reboot
}

main