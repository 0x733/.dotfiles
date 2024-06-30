configure_hyprland() {
  echo "Hyprland yapılandırılıyor..."
  mkdir -p "${CONFIG_DIR}"
  cp "${CONFIG_DIR}/hyprland.conf" "${CONFIG_DIR}/hyprland.conf.bak"
  sed -i -e 's/^bind = CTRL, SPACE, exec, rofi -show combi.*/bind = CTRL, SPACE, exec, wofi/' \
         -e 's/kb_layout = us/kb_layout = tr/' \
         "${CONFIG_DIR}/hyprland.conf"
}
