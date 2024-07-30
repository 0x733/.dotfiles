echo "Yazı tipleri kuruluyor..."
  local font_packages=("noto-fonts" "noto-fonts-cjk" "noto-fonts-emoji" "noto-fonts-extra")
  sudo pacman -Sy --noconfirm "${font_packages[@]}"
  cp "$DOTFILES_DIR/.fonts.conf" "$HOME/"
  cp -r "$DOTFILES_DIR/.fonts" "$HOME/"
  cp -r "$DOTFILES_DIR/.config/fontconfig" "$HOME/.config/"
