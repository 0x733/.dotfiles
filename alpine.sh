#!/bin/sh

# General
doas apk add py3-pip fastfetch android-tools rust npm git wget curl starship

# Python
pip3 install --break-system-packages -U pip yt-dlp setuptools wheel

# Git
git config --global user.email "root@localhost.localdomain"
git config --global user.name "Root"
git config --global credential.helper "cache --timeout=36000"

# ZSH
doas apk add zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
git clone https://github.com/zsh-users/zsh-completions.git ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
rm -rf ~/.zshrc && wget -O ~/.zshrc https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc


# Flatpak
doas apk add flatpak 
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak remote-add --if-not-exists flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo
flatpak update && flatpak upgrade
flatpak install flathub net.mullvad.MullvadBrowser
flatpak install flathub com.brave.Browser
flatpak install flathub io.freetubeapp.FreeTube
flatpak install flathub io.github.mimbrero.WhatsAppDesktop
flatpak install flathub com.mattjakeman.ExtensionManager
flatpak install flathub com.github.ADBeveridge.Raider
flatpak install flathub org.onionshare.OnionShare
flatpak install flathub de.haeckerfelix.Fragments

# Fuck
doas apk del firefox
doas apk del epiphany
