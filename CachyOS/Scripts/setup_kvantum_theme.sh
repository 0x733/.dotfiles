setup_kvantum_theme() {
  echo "Kvantum teması ayarlanıyor..."
  qt5ct & 
  sleep 5
  kvantummanager --set kvantum-dark
  qt5ct --set-window-theme Kvantum
}
