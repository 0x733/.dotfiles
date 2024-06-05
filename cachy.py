import subprocess
import os
import sys
import shutil

# Error Handling
def run_command(command, error_message):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_message}")
        print(e.stderr)
        sys.exit(1)
    return result.stdout

# Log file
LOGFILE = "/var/log/setup_script.log"
sys.stdout = open(LOGFILE, 'a')
sys.stderr = sys.stdout

# Variables
USER = os.getenv("SUDO_USER") or os.getlogin()
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config/hypr")
DOTFILES_DIR = os.path.join(os.path.expanduser("~"), ".dotfiles/.dots")

# Ensure the script is run as the intended user
if os.geteuid() == 0:
    print("Please do not run this script as root. Use your regular user account.")
    sys.exit(1)

def update_system():
    print("Updating system and installing packages...")
    run_command(["sudo", "pacman", "-Syu", "--noconfirm"], "System update failed")

def configure_hyprland():
    print("Configuring Hyprland...")
    hyprland_conf = os.path.join(CONFIG_DIR, "hyprland.conf")
    run_command(["sed", "-i", "s/^bind = CTRL, SPACE, exec, rofi -show combi -modi window,run,emoji,combi -combi-modi window,run,emoji/#&/; s/^#bind = CTRL, SPACE, exec, wofi/bind = CTRL, SPACE, exec, wofi/", hyprland_conf], "Failed to configure Rofi")
    run_command(["sed", "-i", "s/kb_layout = us/kb_layout = tr/", hyprland_conf], "Failed to configure keyboard layout")

def setup_chaotic_aur():
    print("Setting up Chaotic AUR...")
    run_command(["sudo", "pacman-key", "--recv-key", "3056513887B78AEB", "--keyserver", "keyserver.ubuntu.com"], "Failed to receive Chaotic AUR key")
    run_command(["sudo", "pacman-key", "--lsign-key", "3056513887B78AEB"], "Failed to locally sign Chaotic AUR key")
    run_command(["sudo", "pacman", "-U", "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst"], "Failed to install Chaotic keyring")
    run_command(["sudo", "pacman", "-U", "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst"], "Failed to install Chaotic mirrorlist")
    shutil.copy("/etc/pacman.conf", "/etc/pacman.conf.bak")
    with open("/etc/pacman.conf", "a") as pacman_conf:
        pacman_conf.write("\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist")
    print("Configured Chaotic AUR in pacman.conf")

def install_packages():
    print("Installing additional packages...")
    run_command(["sudo", "pacman", "-Sy", "--noconfirm", "--needed", "python-pip", "android-tools", "rust", "npm", "git", "wget", "curl", "starship", "waydroid", "rustdesk"], "Failed to install packages")

def setup_python():
    print("Setting up Python...")
    run_command(["pip3", "install", "--break-system-packages", "-U", "pip", "yt-dlp"], "Failed to install Python packages")

def configure_git():
    print("Configuring Git...")
    run_command(["git", "config", "--global", "user.email", "root@localhost.localdomain"], "Failed to configure Git email")
    run_command(["git", "config", "--global", "user.name", "Root"], "Failed to configure Git username")
    run_command(["git", "config", "--global", "credential.helper", "cache --timeout=36000"], "Failed to configure Git credential helper")

def setup_zsh():
    print("Setting up ZSH...")
    run_command(["sudo", "pacman", "-Sy", "--noconfirm", "--needed", "zsh"], "Failed to install ZSH")
    run_command(["sh", "-c", "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)", "", "--unattended"], "Failed to install Oh My Zsh")
    ZSH_CUSTOM = os.path.expanduser("~/.oh-my-zsh/custom")
    run_command(["git", "clone", "https://github.com/zsh-users/zsh-completions.git", f"{ZSH_CUSTOM}/plugins/zsh-completions"], "Failed to clone zsh-completions")
    run_command(["git", "clone", "https://github.com/zsh-users/zsh-syntax-highlighting.git", f"{ZSH_CUSTOM}/plugins/zsh-syntax-highlighting"], "Failed to clone zsh-syntax-highlighting")
    run_command(["git", "clone", "https://github.com/zsh-users/zsh-autosuggestions.git", f"{ZSH_CUSTOM}/plugins/zsh-autosuggestions"], "Failed to clone zsh-autosuggestions")
    run_command(["rm", "-rf", "~/.zshrc"], "Failed to remove old .zshrc")
    run_command(["wget", "-O", "~/.zshrc", "https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc"], "Failed to download .zshrc")

def setup_flatpak():
    print("Setting up Flatpak...")
    run_command(["sudo", "pacman", "-Sy", "--noconfirm", "--needed", "flatpak"], "Failed to install Flatpak")
    run_command(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"], "Failed to add Flathub remote")
    run_command(["flatpak", "remote-add", "--if-not-exists", "flathub-beta", "https://flathub.org/beta-repo/flathub-beta.flatpakrepo"], "Failed to add Flathub Beta remote")
    run_command(["flatpak", "update", "&&", "flatpak", "upgrade"], "Failed to update Flatpak")

def install_flatpak_apps():
    print("Installing Flatpak apps...")
    apps = [
        "net.mullvad.MullvadBrowser", "com.brave.Browser", "io.github.mimbrero.WhatsAppDesktop",
        "org.onionshare.OnionShare", "de.haeckerfelix.Fragments", "org.videolan.VLC",
        "io.frama.tractor.carburetor", "org.kde.dolphin", "org.kde.ark", "org.DolphinEmu.dolphin-emu"
    ]
    for app in apps:
        run_command(["flatpak", "install", "flathub", app, "-y"], f"Failed to install {app}")

def update_user_dirs():
    print("Updating user directories...")
    run_command(["xdg-user-dirs-update"], "Failed to update user directories")

def setup_fonts():
    print("Setting up fonts...")
    shutil.copy(os.path.join(DOTFILES_DIR, ".fonts.conf"), os.path.expanduser("~"))
    shutil.copytree(os.path.join(DOTFILES_DIR, ".fonts"), os.path.expanduser("~/.fonts"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(DOTFILES_DIR, ".config/fontconfig"), os.path.expanduser("~/.config/fontconfig"), dirs_exist_ok=True)

def install_video_dependencies():
    print("Installing video playback dependencies...")
    run_command(["sudo", "pacman", "-Sy", "--noconfirm", "gstreamer", "gst-plugins-good", "gst-plugins-bad", "gst-plugins-ugly", "gst-libav"], "Failed to install video playback dependencies")

def main():
    update_system()
    configure_hyprland()
    setup_chaotic_aur()
    install_packages()
    setup_python()
    configure_git()
    setup_zsh()
    setup_flatpak()
    install_flatpak_apps()
    update_user_dirs()
    setup_fonts()
    install_video_dependencies()
    print("Setup complete. Rebooting system...")
    run_command(["sudo", "reboot"], "Failed to reboot system")

if __name__ == "__main__":
    main()