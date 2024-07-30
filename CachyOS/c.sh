#!/bin/bash

# Define an array of file extensions to remove
extensions=(
    "*.tmp"
    "*.bak"
    "*.log"
    "*.old"
    "*.swp"
    "*.cache"
    "*.crash"
    "*.gz"
    "*.xz"
)

# Function to securely remove temporary files
shred_temp_files() {
    echo "Securely removing temporary files..."
    sudo find /tmp /var/tmp -type f \( -name "${extensions[@]}" \) -exec shred -u {} \;
    echo "Temporary files removed."
}

# Function to clear zsh history
clear_zsh_history() {
    echo "Clearing zsh command history..."
    rm -f ~/.zsh_history
    touch ~/.zsh_history
    echo "zsh command history cleared."
}

# Function to clean package cache
clean_package_cache() {
    echo "Cleaning package cache..."
    sudo pacman -Sc --noconfirm
    echo "Package cache cleaned."
}

# Function to remove orphan packages
remove_orphans() {
    echo "Removing orphan packages..."
    sudo pacman -Rns $(sudo pacman -Qdtq) --noconfirm
    echo "Orphan packages removed."
}

# Function to perform disk cleanup
disk_cleanup() {
    echo "Performing disk cleanup..."
    sudo rm -rf /var/cache/pacman/pkg/*
    echo "Pacman package cache cleaned."
    sudo find /var/log -type f \( -name "*.log" \) -exec rm -f {} \;
    echo "Log files cleaned."
    sudo find / -type f \( -name "${extensions[@]}" \) -exec rm -f {} \;
    echo "Files with specified extensions cleaned."
}

# Function to clean home cache
clean_home_cache() {
    echo "Cleaning home cache..."
    rm -rf ~/.cache/*
    echo "Home cache cleaned."
}

# Function to perform memory optimization
memory_optimization() {
    echo "Performing memory optimization..."
    sudo sync
    sudo sysctl -w vm.drop_caches=3
    echo "Memory optimization completed."
}

# Function to update the system
system_update() {
    echo "Updating the system..."
    sudo pacman -Syu
    echo "System updated."
}

# Call all functions
shred_temp_files
clear_zsh_history
clean_package_cache
remove_orphans
disk_cleanup
clean_home_cache
memory_optimization
system_update

echo "All operations completed."