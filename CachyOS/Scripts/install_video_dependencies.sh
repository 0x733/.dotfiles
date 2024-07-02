install_video_dependencies() {
  echo "Video oynatma bağımlılıkları kuruluyor..."
  sudo pacman -Sy --noconfirm gstreamer gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
}
