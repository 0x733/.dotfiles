import subprocess
import os
import sys
import shutil

# Error Handling
def run_command(command, error_message):
    try:
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
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
HOME_DIR = os.path.expanduser("~")
ZSH_CUSTOM = os.path.join(HOME_DIR, ".oh-my-zsh/custom")

# Ensure the script is run as the intended user
if os.geteuid() == 0:
    print("Please do not run this script as root. Use your regular user account.")
    sys.exit(1)

def check_dependencies():
    print("Checking for required dependencies...")
    required_cmds = ["doas", "flatpak"]
    for cmd in required_cmds:
        if not shutil.which(cmd):
            print(f"{cmd} is required but it's not installed. Aborting.")
            sys.exit(1)

def install_general_packages():
    print("Installing general packages...")
    run_command(["doas", "apk", "add", "py3-pip", "fastfetch", "android-tools", "rust", "npm", "git", "wget", "curl", "starship"], "Failed to install general packages")

def setup_python():
    print("Setting up Python...")
    run_command(["pip3", "install", "--break-system-packages", "-U", "pip", "yt-dlp", "setuptools", "wheel"], "Failed to install Python packages")

def configure_git():
    print("Configuring Git...")
    run_command(["git", "config", "--global", "user.email", "root@localhost.localdomain"], "Failed to configure Git email")
    run_command(["git", "config", "--global", "user.name", "Root"], "Failed to configure Git username")
    run_command(["git", "config", "--global", "credential.helper", "cache --timeout=36000"], "Failed to configure Git credential helper")

def setup_zsh():
    print("Setting up ZSH...")
    run_command(["doas", "apk", "add", "zsh"], "Failed to install ZSH")
    run_command(["sh", "-c", "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)", "", "--unattended"], "Failed to install Oh My Zsh")
    run_command(["git", "clone", "https://github.com/zsh-users/zsh-completions.git", os.path.join(ZSH_CUSTOM, "plugins/zsh-completions")], "Failed to clone zsh-completions")
    run_command(["git", "clone", "https://github.com/zsh-users/zsh-syntax-highlighting.git", os.path.join(ZSH_CUSTOM, "plugins/zsh-syntax-highlighting")], "Failed to clone zsh-syntax-highlighting")
    run_command(["git", "clone", "https://github.com/zsh-users/zsh-autosuggestions.git", os.path.join(ZSH_CUSTOM, "plugins/zsh-autosuggestions")], "Failed to clone zsh-autosuggestions")
    run_command(["rm", "-rf", os.path.join(HOME_DIR, ".zshrc")], "Failed to remove old .zshrc")
    run_command(["wget", "-O", os.path.join(HOME_DIR, ".zshrc"), "https://raw.githubusercontent.com/0x733/.dotfiles/main/.dots/.zshrc"], "Failed to download .zshrc")

def setup_flatpak():
    print("Setting up Flatpak...")
    run_command(["doas", "apk", "add", "flatpak"], "Failed to install Flatpak")
    run_command(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"], "Failed to add Flathub remote")
    run_command(["flatpak", "remote-add", "--if-not-exists", "flathub-beta", "https://flathub.org/beta-repo/flathub-beta.flatpakrepo"], "Failed to add Flathub Beta remote")
    run_command(["flatpak", "update"], "Failed to update Flatpak")
    run_command(["flatpak", "upgrade"], "Failed to upgrade Flatpak")

def install_flatpak_apps():
    print("Installing Flatpak apps...")
    apps = [
        "net.mullvad.MullvadBrowser", "com.brave.Browser", "io.github.mimbrero.WhatsAppDesktop",
        "com.mattjakeman.ExtensionManager", "com.github.ADBeveridge.Raider",
        "org.onionshare.OnionShare", "de.haeckerfelix.Fragments", "org.videolan.VLC"
    ]
    for app in apps:
        run_command(["flatpak", "install", "flathub", app, "-y"], f"Failed to install {app}")

def remove_unwanted_packages():
    print("Removing unwanted packages...")
    run_command(["doas", "apk", "del", "firefox"], "Failed to remove Firefox")
    run_command(["doas", "apk", "del", "epiphany"], "Failed to remove Epiphany")

def update_user_dirs():
    print("Updating user directories...")
    run_command(["xdg-user-dirs-update"], "Failed to update user directories")

def main():
    check_dependencies()
    install_general_packages()
    setup_python()
    configure_git()
    setup_zsh()
    setup_flatpak()
    install_flatpak_apps()
    update_user_dirs()
    remove_unwanted_packages()
    print("Setup complete. Rebooting system...")
    run_command(["doas", "reboot"], "Failed to reboot system")

if __name__ == "__main__":
    main()