import curses,subprocess,time,os
from datetime import datetime

def run_command(cmd): subprocess.run(f"sudo {cmd}",shell=True)
def show_progress(stdscr,total_steps): stdscr.clear();stdscr.addstr(0,0,"İşlem devam ediyor...");[stdscr.addstr(2,0,"["+"#"*i+"-"*(total_steps-i-1)+"]");stdscr.refresh();time.sleep(0.1) for i in range(total_steps)]
def create_backup(): d=f"/nix/backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"; run_command(f"mkdir -p {d}");run_command(f"sudo cp -r /nix/store {d}");return d
def restore_backup(d): run_command(f"sudo cp -r {d}/* /nix/store")
def list_flatpak_apps(): return subprocess.run(["flatpak","list","--app"],stdout=subprocess.PIPE,text=True).stdout.splitlines()
def flatpak_clean_remove(app): run_command(f"flatpak uninstall --delete-data {app}");run_command("flatpak remove --unused");run_command(f"rm -rf ~/.var/app/{app} ~/.cache/{app}")
def schedule_cleanup(stdscr,h): show_progress(stdscr,5);[time.sleep(h*3600);run_command("sudo nix-collect-garbage -d");run_command("sudo nix-store --gc")]

def main(stdscr):
    options=["1. Eski paketleri temizle (NixOS)","2. Flatpak temizliği","3. Flatpak önbellek temizliği","4. Yedekleme yap","5. Geri yükleme","6. Temizlik zamanlayıcısı ayarla","7. Çık"]
    current_row=0

    def print_menu():
        stdscr.clear()
        for idx,option in enumerate(options): stdscr.addstr(idx,0,option,curses.A_REVERSE if idx==current_row else curses.A_NORMAL)
        stdscr.refresh()

    def flatpak_cleanup_menu():
        apps=list_flatpak_apps()
        if not apps: stdscr.addstr(0,0,"Yüklü Flatpak uygulaması bulunamadı.");stdscr.refresh();stdscr.getch();return
        stdscr.addstr(0,0,"Silmek istediğiniz Flatpak paketini seçin (q ile çık):")
        app_selected=0
        while True:
            for idx,app in enumerate(apps): stdscr.addstr(idx+1,0,app,curses.A_REVERSE if idx==app_selected else curses.A_NORMAL)
            stdscr.refresh()
            key=stdscr.getch()
            if key==curses.KEY_UP: app_selected=(app_selected-1)%len(apps)
            elif key==curses.KEY_DOWN: app_selected=(app_selected+1)%len(apps)
            elif key==10: app_to_remove=apps[app_selected];flatpak_clean_remove(app_to_remove);stdscr.addstr(len(apps)+1,0,f"{app_to_remove} temizlendi.");stdscr.refresh();stdscr.getch();break
            elif key==ord('q'): break

    print_menu()

    while True:
        key=stdscr.getch()
        if key==curses.KEY_UP: current_row=(current_row-1)%len(options)
        elif key==curses.KEY_DOWN: current_row=(current_row+1)%len(options)
        elif key==10:
            if current_row==0: run_command("nix-collect-garbage -d")
            elif current_row==1: flatpak_cleanup_menu()
            elif current_row==2: run_command("rm -rf ~/.var/app/*/cache/*")
            elif current_row==3: backup_dir=create_backup();stdscr.addstr(len(options),0,f"Sistem yedeklendi: {backup_dir}");stdscr.refresh();stdscr.getch()
            elif current_row==4: stdscr.addstr(0,0,"Yedeği geri yüklemek için dizin girin:");curses.echo();backup_dir=stdscr.getstr(1,0).decode('utf-8');restore_backup(backup_dir);curses.noecho();stdscr.addstr(2,0,"Yedek geri yüklendi.");stdscr.refresh();stdscr.getch()
            elif current_row==5: stdscr.addstr(0,0,"Zamanlayıcı (saat cinsinden) girin: ");curses.echo();hours=stdscr.getstr(1,0).decode('utf-8');curses.noecho();schedule_cleanup(stdscr,int(hours)) if hours.isdigit() else stdscr.addstr(2,0,"Geçersiz giriş");stdscr.refresh();stdscr.getch()
            elif current_row==6: break
            print_menu()

curses.wrapper(main)