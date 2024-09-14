import curses,random,string
def generate_password(length,u,l,n,s,e,symbols):
    c=(string.ascii_uppercase if u else'')+(string.ascii_lowercase if l else'')+(string.digits if n else'')+(symbols if s else'')
    if not c or(e and len(set(c))<length):return None
    p,used='',set()
    while len(p)<length:
        ch=random.choice(c)
        if e and ch in used:continue
        p+=ch;used.add(ch)
    return p
def main(stdscr):
    stdscr.addstr(0,0,"Dil seçin: (E) English, (T) Türkçe");stdscr.refresh()
    lang='tr'if stdscr.getch()in[ord('T'),ord('t')]else'en';curses.curs_set(0);stdscr.clear()
    l,u,lc,n,s,e,p,symbols=12,True,True,True,True,True,'',string.punctuation
    selected_row=1
    def print_menu():
        stdscr.clear()
        if lang=='tr':
            stdscr.addstr(0,0,"Şifre Oluşturucu")
            stdscr.addstr(1,0,"Yön tuşlarıyla gezin, Enter ile değiştir.")
            stdscr.addstr(2,0,"'q' ile çık.")
            stdscr.addstr(4,0,f"1. Uzunluk: {l}",curses.A_REVERSE if selected_row==3 else curses.A_NORMAL)
            stdscr.addstr(5,0,f"2. Büyük Harf: {'Evet'if u else'Hayır'}",curses.A_REVERSE if selected_row==4 else curses.A_NORMAL)
            stdscr.addstr(6,0,f"3. Küçük Harf: {'Evet'if lc else'Hayır'}",curses.A_REVERSE if selected_row==5 else curses.A_NORMAL)
            stdscr.addstr(7,0,f"4. Rakam: {'Evet'if n else'Hayır'}",curses.A_REVERSE if selected_row==6 else curses.A_NORMAL)
            stdscr.addstr(8,0,f"5. Sembol: {'Evet'if s else'Hayır'},{symbols}",curses.A_REVERSE if selected_row==7 else curses.A_NORMAL)
            stdscr.addstr(9,0,f"6. Tekrar Yok: {'Evet'if e else'Hayır'}",curses.A_REVERSE if selected_row==8 else curses.A_NORMAL)
            stdscr.addstr(11,0,"Şifre: ");stdscr.addstr(12,0,p if p else"Şifre oluşturulmadı.")
        else:
            stdscr.addstr(0,0,"Password Generator")
            stdscr.addstr(1,0,"Use arrows, Enter to change.")
            stdscr.addstr(2,0,"'q' to quit.")
            stdscr.addstr(4,0,f"1. Length: {l}",curses.A_REVERSE if selected_row==3 else curses.A_NORMAL)
            stdscr.addstr(5,0,f"2. Uppercase: {'Yes'if u else'No'}",curses.A_REVERSE if selected_row==4 else curses.A_NORMAL)
            stdscr.addstr(6,0,f"3. Lowercase: {'Yes'if lc else'No'}",curses.A_REVERSE if selected_row==5 else curses.A_NORMAL)
            stdscr.addstr(7,0,f"4. Numbers: {'Yes'if n else'No'}",curses.A_REVERSE if selected_row==6 else curses.A_NORMAL)
            stdscr.addstr(8,0,f"5. Symbols: {'Yes'if s else'No'},{symbols}",curses.A_REVERSE if selected_row==7 else curses.A_NORMAL)
            stdscr.addstr(9,0,f"6. No Repeats: {'Yes'if e else'No'}",curses.A_REVERSE if selected_row==8 else curses.A_NORMAL)
            stdscr.addstr(11,0,"Password: ");stdscr.addstr(12,0,p if p else"No password generated.")
        stdscr.addstr(14,0,"'g' ile şifre oluştur.")
    print_menu()
    while True:
        k=stdscr.getch()
        if k==curses.KEY_UP:selected_row=(selected_row-1)%10
        elif k==curses.KEY_DOWN:selected_row=(selected_row+1)%10
        elif k==10:
            if selected_row==3:
                stdscr.clear();stdscr.addstr(0,0,"Şifre uzunluğunu gir (max 128): ");stdscr.refresh();curses.echo()
                length_input=stdscr.getstr(0,32).decode('utf-8')
                if length_input.isdigit():l=min(int(length_input),128)
                else:stdscr.addstr(1,0,"Geçersiz giriş.");stdscr.refresh();curses.napms(1000)
                curses.noecho()
            elif selected_row==4:u=not u
            elif selected_row==5:lc=not lc
            elif selected_row==6:n=not n
            elif selected_row==7:
                s=not s
                if s:
                    stdscr.clear();stdscr.addstr(0,0,"Sembolleri gir: ");stdscr.refresh();curses.echo()
                    symbols_input=stdscr.getstr(0,20).decode('utf-8')
                    symbols=symbols_input if symbols_input else string.punctuation
                    curses.noecho()
            elif selected_row==8:e=not e
        elif k==ord('g'):
            if not(u or lc or n or s):stdscr.addstr(1,0,"En az bir karakter seçmelisiniz.");stdscr.refresh();curses.napms(1000)
            else:p=generate_password(l,u,lc,n,s,e,symbols)
        elif k==ord('q'):break
        print_menu();stdscr.refresh()
curses.wrapper(main)