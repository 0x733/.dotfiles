echo "Black Arch kuruluyor..."
  curl -O https://blackarch.org/strap.sh
  echo "5f3d815e424213e9b6b278a859f6d47426f0b3b0 strap.sh" | sha1sum -c -
  chmod +x strap.sh
  sudo ./strap.sh
  rm strap.sh
