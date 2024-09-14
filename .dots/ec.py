import curses, random, string
def generate_password(length,u,l,n,s,e,symbols):
    c=(string.ascii_uppercase if u else '')+(string.ascii_lowercase if l else '')+(string.digits if n else '')+(symbols if s else '')
    if e and len(set(c))<length:return None
    p,used="",set()
    while len(p)<length:
        ch=random.choice(c)
        if e and ch in used:continue
        p+=ch;used.add(ch)
    return p
def main(stdscr):
    stdscr.addstr(0,0,"Lütfen dil seçin: (E) English, (T) Türkçe");stdscr.refresh();lang_key=stdscr.getch()
    lang='tr'if lang_key==ord('T')or lang_key==ord('t')else'en';curses.curs_set(0);stdscr.clear()
    l,u,lc,n,s,e,p,symbols=12,True,True,True,True,True,"",string.punctuation
    while 1:
        stdscr.clear()
        if lang=='tr':
            stdscr.addstr(0,0,"Gelişmiş Şifre Oluşturucu (Terminal)")
            stdscr.addstr(1,0,"Gezinmek için yön tuşlarını kullanın, seçenekleri değiştirmek için Enter'a basın.")
            stdscr.addstr(2,0,"Çıkmak için 'q' tuşuna basın.");stdscr.addstr(4,0,f"1. Şifre Uzunluğu: {l} (Değiştirmek için Enter)")
            stdscr.addstr(5,0,f"2. Büyük Harfler (A-Z): {'Evet'if u else 'Hayır'}");stdscr.addstr(6,0,f"3. Küçük Harfler (a-z): {'Evet'if lc else 'Hayır'}")
            stdscr.addstr(7,0,f"4. Rakamlar (0-9): {'Evet'if n else 'Hayır'}");stdscr.addstr(8,0,f"5. Semboller (@-$): {'Evet'if s else 'Hayır'}, Semboller: {symbols}")
            stdscr.addstr(9,0,f"6. Tekrarlayan Karakterler Hariç Tutulsun: {'Evet'if e else 'Hayır'}")
            stdscr.addstr(11,0,"Oluşturulan Şifre: ");stdscr.addstr(12,0,f"{p}"if p else "Geçersiz ayarlar!")
            stdscr.addstr(14,0,"Mevcut ayarlarla yeni bir şifre oluşturmak için 'g' tuşuna basın.")
        else:
            stdscr.addstr(0,0,"Advanced Password Generator (Terminal)");stdscr.addstr(1,0,"Use arrow keys to navigate, press Enter to change options.")
            stdscr.addstr(2,0,"Press 'q' to exit.");stdscr.addstr(4,0,f"1. Password Length: {l} (Press Enter to change)")
            stdscr.addstr(5,0,f"2. Include Uppercase Letters (A-Z): {'Yes'if u else 'No'}");stdscr.addstr(6,0,f"3. Include Lowercase Letters (a-z): {'Yes'if lc else 'No'}")
            stdscr.addstr(7,0,f"4. Include Numbers (0-9): {'Yes'if n else 'No'}");stdscr.addstr(8,0,f"5. Include Symbols (@-$): {'Yes'if s else 'No'}, Symbols: {symbols}")
            stdscr.addstr(9,0,f"6. Exclude Duplicate Characters: {'Yes'if e else 'No'}")
            stdscr.addstr(11,0,"Generated Password: ");stdscr.addstr(12,0,f"{p}"if p else "Invalid settings!")
            stdscr.addstr(14,0,"Press 'g' to generate a new password.")
        k=stdscr.getch()
        if k==ord('1'):
            stdscr.clear();stdscr.addstr(0,0,"Şifre uzunluğunu girin: ");stdscr.refresh();curses.echo();length_input=stdscr.getstr(0,24).decode('utf-8')
            if length_input.isdigit():l=int(length_input)
            else:stdscr.addstr(1,0,"Geçersiz giriş, lütfen sayı girin.");stdscr.refresh();curses.napms(1000)
            curses.noecho()
        elif k==ord('2'):u=not u
        elif k==ord('3'):lc=not lc
        elif k==ord('4'):n=not n
        elif k==ord('5'):
            s=not s
            if s:
                stdscr.clear();stdscr.addstr(0,0,"Kullanılacak sembolleri girin: ");stdscr.refresh();curses.echo();symbols_input=stdscr.getstr(0,32).decode('utf-8')
                symbols=symbols_input if symbols_input else string.punctuation
                curses.noecho()
        elif k==ord('6'):e=not e
        elif k==ord('g'):
            if not (u or lc or n or s):
                stdscr.addstr(1,0,"Hata: En az bir karakter türü seçilmelidir.");stdscr.refresh();curses.napms(1000)
            else:
                p=generate_password(l,u,lc,n,s,e,symbols)
        elif k==ord('q'):break
        stdscr.refresh()
curses.wrapper(main)