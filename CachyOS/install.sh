#!/bin/bash
set -euo pipefail

DOTFILES_DIR="$HOME/.dotfiles"
XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"

# Chaotic AUR key and repository setup
sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com && 
sudo pacman-key --lsign-key 3056513887B78AEB && 
sudo pacman -U --noconfirm \
    'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' \
    'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'

# Add Chaotic AUR to pacman.conf
echo "[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist" | sudo tee -a /etc/pacman.conf

# System update and package installation
sudo pacman -Syu --noconfirm \
    git wget curl xdg-user-dirs playerctl unzip zip p7zip unrar tar rsync \
    qt5ct kvantum gvfs gvfs-smb gvfs-mtp gvfs-afc gvfs-goa gvfs-google \
    gvfs-gphoto2 gvfs-nfs brave-bin librewolf onionshare vlc dolphin-emu \
    yt-dlp starship waydroid chatgpt-desktop-bin ferdium-bin rustdesk \
    visual-studio-code-bin noto-fonts noto-fonts-cjk noto-fonts-emoji \
    noto-fonts-extra gstreamer gst-plugins-good gst-plugins-bad \
    gst-plugins-ugly gst-libav qt6-svg qt6-declarative

# Git configuration
git config --global user.email "root@localhost.localdomain"
git config --global user.name "Root"
git config --global credential.helper store

# Hyprland configuration
mkdir -p "${XDG_CONFIG_HOME}/hypr"
if [[ -f "${XDG_CONFIG_HOME}/hypr/hyprland.conf" ]]; then
    cp "${XDG_CONFIG_HOME}/hypr/hyprland.conf" "${XDG_CONFIG_HOME}/hypr/hyprland.conf.bak"
fi

sed -i \
    -e 's/^bind = CTRL, SPACE, exec, rofi -show combi.*/bind = CTRL, SPACE, exec, wofi/' \
    -e 's/kb_layout = us/kb_layout = tr/' \
    "${XDG_CONFIG_HOME}/hypr/hyprland.conf"

# User directories update
xdg-user-dirs-update

# Font configuration
cp "$DOTFILES_DIR/.dots/.fonts.conf" "$HOME/"
cp -r "$DOTFILES_DIR/.dots/.fonts" "$HOME/"
cp -r "$DOTFILES_DIR/.dots/.config/fontconfig" "$HOME/.config/"

# Zsh and Oh-My-Zsh installation
if ! command -v zsh &> /dev/null; then
    sudo pacman -Sy --noconfirm --needed zsh
fi

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"
git clone --depth 1 https://github.com/zsh-users/zsh-completions "$ZSH_CUSTOM/plugins/zsh-completions"
git clone --depth 1 https://github.com/zsh-users/zsh-syntax-highlighting "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
git clone --depth 1 https://github.com/zsh-users/zsh-autosuggestions "$ZSH_CUSTOM/plugins/zsh-autosuggestions"

wget -q --show-progress --progress=bar:force:noscroll -O ~/.zshrc https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc
chsh -s /bin/zsh

# SDDM theme setup
THEME_URL="https://github.com/catppuccin/sddm/releases/download/v1.0.0/catppuccin-mocha.zip"
sudo wget -P /usr/share/sddm/themes/ $THEME_URL && 
sudo unzip /usr/share/sddm/themes/catppuccin-mocha.zip -d /usr/share/sddm/themes/ && 
sudo rm /usr/share/sddm/themes/catppuccin-mocha.zip

sudo sed -i '/\[Theme\]/,+1 s/Current=.*/Current=catppuccin-mocha/' /etc/sddm.conf || \
sudo bash -c 'echo -e "[Theme]\nCurrent=catppuccin-mocha" >> /etc/sddm.conf'

sudo systemctl restart sddm

echo "Installation complete!"