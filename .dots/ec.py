import curses
import random
import string
from typing import Optional, Dict

def generate_password(config: Dict) -> Optional[str]:
    char_sets = {
        'upper': string.ascii_uppercase if config['uppercase'] else '',
        'lower': string.ascii_lowercase if config['lowercase'] else '',
        'digits': string.digits if config['numbers'] else '',
        'symbols': config['symbol_chars'] if config['symbols'] else ''
    }
    chars = ''.join(char_sets.values())
    
    if not chars:
        return None
        
    if config['no_repeat']:
        unique_chars = list(set(chars))
        return ''.join(random.sample(unique_chars, config['length'])) if len(unique_chars) >= config['length'] else None
    
    return ''.join(random.choice(chars) for _ in range(config['length']))

def get_menu_text(config: Dict, selected_row: int, lang: str) -> list:
    menu = {
        'tr': [
            ('Şifre Oluşturucu', 0),
            (f"1. Uzunluk: {config['length']}", 3),
            (f"2. Büyük Harf: {'Evet' if config['uppercase'] else 'Hayır'}", 4),
            (f"3. Küçük Harf: {'Evet' if config['lowercase'] else 'Hayır'}", 5),
            (f"4. Rakam: {'Evet' if config['numbers'] else 'Hayır'}", 6),
            (f"5. Sembol: {'Evet' if config['symbols'] else 'Hayır'},{config['symbol_chars']}", 7),
            (f"6. Tekrar Yok: {'Evet' if config['no_repeat'] else 'Hayır'}", 8),
            ("Şifre: ", 11),
            (config['password'] if config['password'] else "Şifre oluşturulmadı.", 12),
            ("'g' ile şifre oluştur, 'q' ile çık.", 14)
        ],
        'en': [
            ('Password Generator', 0),
            (f"1. Length: {config['length']}", 3),
            (f"2. Uppercase: {'Yes' if config['uppercase'] else 'No'}", 4),
            (f"3. Lowercase: {'Yes' if config['lowercase'] else 'No'}", 5),
            (f"4. Numbers: {'Yes' if config['numbers'] else 'No'}", 6),
            (f"5. Symbols: {'Yes' if config['symbols'] else 'No'},{config['symbol_chars']}", 7),
            (f"6. No Repeats: {'Yes' if config['no_repeat'] else 'No'}", 8),
            ("Password: ", 11),
            (config['password'] if config['password'] else "No password generated.", 12),
            ("Press 'g' to generate, 'q' to quit.", 14)
        ]
    }
    return menu[lang]

def display_menu(stdscr, config: Dict, selected_row: int, lang: str) -> None:
    stdscr.clear()
    for text, row in get_menu_text(config, selected_row, lang):
        attr = curses.A_REVERSE if 3 <= row <= 8 and row == selected_row else curses.A_NORMAL
        stdscr.addstr(row, 0, text, attr)
    stdscr.refresh()

def handle_input(stdscr, config: Dict, selected_row: int, lang: str) -> None:
    if selected_row == 3:
        stdscr.clear()
        prompt = "Şifre uzunluğunu gir (max 128): " if lang == 'tr' else "Enter password length (max 128): "
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        curses.echo()
        length_input = stdscr.getstr(0, len(prompt)).decode('utf-8')
        curses.noecho()
        if length_input.isdigit():
            config['length'] = min(int(length_input), 128)
    else:
        toggle_map = {
            4: 'uppercase',
            5: 'lowercase',
            6: 'numbers',
            7: 'symbols',
            8: 'no_repeat'
        }
        if selected_row in toggle_map:
            key = toggle_map[selected_row]
            config[key] = not config[key]
            if key == 'symbols' and config[key]:
                stdscr.clear()
                prompt = "Sembolleri gir: " if lang == 'tr' else "Enter symbols: "
                stdscr.addstr(0, 0, prompt)
                stdscr.refresh()
                curses.echo()
                symbols_input = stdscr.getstr(0, 20).decode('utf-8')
                curses.noecho()
                config['symbol_chars'] = symbols_input if symbols_input else string.punctuation

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Dil seçin / Select language: (E) English, (T) Türkçe")
    stdscr.refresh()
    
    lang = 'tr' if stdscr.getch() in [ord('T'), ord('t')] else 'en'
    curses.curs_set(0)
    
    config = {
        'length': 12,
        'uppercase': True,
        'lowercase': True,
        'numbers': True,
        'symbols': True,
        'no_repeat': True,
        'symbol_chars': string.punctuation,
        'password': ''
    }
    
    selected_row = 3
    
    while True:
        display_menu(stdscr, config, selected_row, lang)
        key = stdscr.getch()
        
        if key == ord('q'):
            break
        elif key == ord('g'):
            if not any([config['uppercase'], config['lowercase'], config['numbers'], config['symbols']]):
                error_msg = "En az bir karakter seçmelisiniz." if lang == 'tr' else "Select at least one character type."
                stdscr.addstr(1, 0, error_msg)
                stdscr.refresh()
                curses.napms(1000)
            else:
                config['password'] = generate_password(config) or config['password']
        elif key == curses.KEY_UP:
            selected_row = (selected_row - 1) if selected_row > 3 else 8
        elif key == curses.KEY_DOWN:
            selected_row = (selected_row + 1) if selected_row < 8 else 3
        elif key == 10:
            handle_input(stdscr, config, selected_row, lang)

if __name__ == '__main__':
    curses.wrapper(main)