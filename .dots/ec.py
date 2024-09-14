import curses,random,string
def generate_password(length,u,l,n,s,e,symbols):
    c=(string.ascii_uppercase if u else '')+(string.ascii_lowercase if l else '')+(string.digits if n else '')+(symbols if s else '')
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
    while True:
        stdscr.clear()
        if lang=='tr':
            stdscr.addstr(0,0,"Şifre Oluşturucu")
            stdscr.addstr(1,0,"Yön tuşlarıyla gezin, Enter ile değiştir.")
            stdscr.addstr(2,0,"'q' ile çık.")
            stdscr.addstr(4,0,f"1. Uzunluk: {l}")
            stdscr.addstr(5,0,f"2. Büyük Harf: {'Evet'if u else 'Hayır'}")
            stdscr.addstr(6,0,f"3. Küçük Harf: {'Evet'if lc else 'Hayır'}")
            stdscr.addstr(7,0,f"4. Rakam: {'Evet'if n else 'Hayır'}")
            stdscr.addstr(8,0,f"5. Sembol: {'Evet'if s else 'Hayır'},{symbols}")
            stdscr.addstr(9,0,f"6. Tekrar Yok: {'Evet'if e else 'Hayır'}")
            stdscr.addstr(11,0,"Şifre: ");stdscr.addstr(12,0,p if p else "Şifre oluşturulmadı.")
        else:
            stdscr.addstr(0,0,"Password Generator")
            stdscr.addstr(1,0,"Use arrows, Enter to change.")
            stdscr.addstr(2,0,"'q' to quit.")
            stdscr.addstr(4,0,f"1. Length: {l}")
            stdscr.addstr(5,0,f"2. Uppercase: {'Yes'if u else 'No'}")
            stdscr.addstr(6,0,f"3. Lowercase: {'Yes'if lc else 'No'}")
            stdscr.addstr(7,0,f"4. Numbers: {'Yes'if n else 'No'}")
            stdscr.addstr(8,0,f"5. Symbols: {'Yes'if s else 'No'},{symbols}")
            stdscr.addstr(9,0,f"6. No Repeats: {'Yes'if e else 'No'}")
            stdscr.addstr(11,0,"Password: ");stdscr.addstr(12,0,p if p else "No password generated.")
        stdscr.addstr(14,0,"'g' ile şifre oluştur.")
        k=stdscr.getch()
        if k==ord('1'):
            stdscr.clear();stdscr.addstr(0,0,"Şifre uzunluğunu gir (max 128): ");stdscr.refresh();curses.echo()
            length_input=stdscr.getstr(0,32).decode('utf-8')
            if length_input.isdigit():l=min(int(length_input),128)
            else:stdscr.addstr(1,0,"Geçersiz giriş.");stdscr.refresh();curses.napms(1000)
            curses.noecho()
        elif k==ord('2'):u=not u
        elif k==ord('3'):lc=not lc
        elif k==ord('4'):n=not n
        elif k==ord('5'):
            s=not s
            if s:
                stdscr.clear();stdscr.addstr(0,0,"Sembolleri gir: ");stdscr.refresh();curses.echo()
                symbols_input=stdscr.getstr(0,20).decode('utf-8')
                symbols=symbols_input if symbols_input else string.punctuation
                curses.noecho()
        elif k==ord('6'):e=not e
        elif k==ord('g'):
            if not(u or lc or n or s):stdscr.addstr(1,0,"En az bir karakter seçmelisiniz.");stdscr.refresh();curses.napms(1000)
            else:p=generate_password(l,u,lc,n,s,e,symbols)
        elif k==ord('q'):break
        stdscr.refresh()
curses.wrapper(main)