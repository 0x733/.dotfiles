setup_zsh() {
  echo "ZSH kuruluyor..."
  sudo pacman -Sy --noconfirm --needed zsh
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

  # ZSH_CUSTOM dizinini tanımlayın
  ZSH_CUSTOM=${ZSH_CUSTOM:-~/.oh-my-zsh/custom}

  # Eklenti dizinlerinin var olduğundan emin olun
  mkdir -p $ZSH_CUSTOM/plugins/zsh-completions
  mkdir -p $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
  mkdir -p $ZSH_CUSTOM/plugins/zsh-autosuggestions

  # Eklentileri klonlayın
  git clone --depth 1 https://github.com/zsh-users/zsh-completions.git $ZSH_CUSTOM/plugins/zsh-completions
  git clone --depth 1 https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
  git clone --depth 1 https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions

  # .zshrc yapılandırma dosyasını indirin
  rm -rf ~/.zshrc && wget -q --show-progress --progress=bar:force:noscroll -O ~/.zshrc https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc

  # ZSH kabuğunu varsayılan kabuk olarak ayarlayın
  chsh -s /bin/zsh
}
