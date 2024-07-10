#!/bin/bash

# Black Arch ve Chaotic AUR kurulumu
curl -O https://blackarch.org/strap.sh && \
echo "5f3d815e424213e9b6b278a859f6d47426f0b3b0 strap.sh" | sha1sum -c - && \
chmod +x strap.sh && sudo ./strap.sh && rm strap.sh && \
sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com && \
sudo pacman-key --lsign-key 3056513887B78AEB && \
sudo pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' \
                            'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst' && \
sudo sed -i '/\[multilib\]/,+3 s/^#//' /etc/pacman.conf

# Sistem güncelleme ve paket yükleme
sudo pacman -Syu --noconfirm git wget curl xdg-user-dirs playerctl unzip zip p7zip unrar tar rsync qt5ct kvantum gvfs gvfs-smb gvfs-mtp gvfs-afc gvfs-goa gvfs-google gvfs-gphoto2 gvfs-nfs \
brave-bin librewolf onionshare vlc dolphin-emu yt-dlp starship waydroid chatgpt-desktop-bin ferdium-bin rustdesk visual-studio-code-bin noto-fonts noto-fonts-cjk noto-fonts-emoji noto-fonts-extra \
gstreamer gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav qt6-svg qt6-declarative

# Git ve Hyprland yapılandırması
git config --global user.email "root@localhost.localdomain" && \
git config --global user.name "Root" && \
git config --global credential.helper store && \
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/hypr" && \
cp "${XDG_CONFIG_HOME:-$HOME/.config}/hypr/hyprland.conf" "${XDG_CONFIG_HOME:-$HOME/.config}/hypr/hyprland.conf.bak" && \
sed -i -e 's/^bind = CTRL, SPACE, exec, rofi -show combi.*/bind = CTRL, SPACE, exec, wofi/' \
       -e 's/kb_layout = us/kb_layout = tr/' \
       "${XDG_CONFIG_HOME:-$HOME/.config}/hypr/hyprland.conf"

# Yazı tipi ve ZSH kurulumları
xdg-user-dirs-update && \
cp "$DOTFILES_DIR/.fonts.conf" "$HOME/" && \
cp -r "$DOTFILES_DIR/.fonts" "$HOME/" && \
cp -r "$DOTFILES_DIR/.config/fontconfig" "$HOME/.config/" && \
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}" && \
git clone --depth 1 https://github.com/zsh-users/zsh-completions.git "$ZSH_CUSTOM/plugins/zsh-completions" && \
git clone --depth 1 https://github.com/zsh-users/zsh-syntax-highlighting.git "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting" && \
git clone --depth 1 https://github.com/zsh-users/zsh-autosuggestions.git "$ZSH_CUSTOM/plugins/zsh-autosuggestions" && \
rm -rf ~/.zshrc && wget -q --show-progress --progress=bar:force:noscroll -O ~/.zshrc https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc && \
chsh -s /bin/zsh

# SDDM Tema Kurulumu
sudo wget -P /usr/share/sddm/themes/ https://github.com/catppuccin/sddm/releases/download/v1.0.0/catppuccin-mocha.zip && \
sudo unzip /usr/share/sddm/themes/catppuccin-mocha.zip -d /usr/share/sddm/themes/ && \
sudo rm /usr/share/sddm/themes/catppuccin-mocha.zip && \
sudo sed -i '/\[Theme\]/,+1 s/Current=.*/Current=catppuccin-mocha/' /etc/sddm.conf || sudo sh -c 'echo "[Theme]\nCurrent=catppuccin-mocha" >> /etc/sddm.conf' && \
sudo systemctl restart sddm