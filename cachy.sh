#!/bin/sh

#Rofi
sed -i 's/^bind = CTRL, SPACE, exec, rofi -show combi -modi window,run,emoji,combi -combi-modi window,run,emoji/#&/; s/^#bind = CTRL, SPACE, exec, wofi/bind = CTRL, SPACE, exec, wofi/' ~/.config/hypr/hyprland.conf

# Keyboard
sed -i 's/kb_layout = us/kb_layout = tr/' ~/.config/hypr/hyprland.conf

# Chaotic Aur
sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
sudo pacman-key --lsign-key 3056513887B78AEB
sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'
echo -e "\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist" | sudo tee -a /etc/pacman.conf

# Packages 
sudo pacman -S python-pip android-tools rust npm git wget curl starship -y

# Python
pip3 install --break-system-packages -U pip yt-dlp

# Git
git config --global user.email "root@localhost.localdomain"
git config --global user.name "Root"
git config --global credential.helper "cache --timeout=36000"

# ZSH
sudo pacman -S zsh -y
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
git clone https://github.com/zsh-users/zsh-completions.git ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
rm -rf ~/.zshrc && wget -O ~/.zshrc https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc

# Flatpak
sudo pacman -S flatpak -y
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak remote-add --if-not-exists flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo
flatpak update && flatpak upgrade
flatpak install flathub net.mullvad.MullvadBrowser
flatpak install flathub com.brave.Browser
flatpak install flathub io.freetubeapp.FreeTube
flatpak install flathub io.github.mimbrero.WhatsAppDesktop
flatpak install flathub org.onionshare.OnionShare
flatpak install flathub de.haeckerfelix.Fragments
flatpak install flathub org.videolan.VLC
xdg-user-dirs-update

# Font
cp ~/.dotfiles/.dots/.fonts.conf /home/user/
cp -r ~/.dotfiles/.dots/.fonts /home/user/
cp -r ~/.dotfiles/.dots/.config/fontconfig ~/.config/

reboot
