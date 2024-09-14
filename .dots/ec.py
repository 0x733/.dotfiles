import curses, random, string
def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols, exclude_duplicates):
    characters = (string.ascii_uppercase if use_uppercase else '') + (string.ascii_lowercase if use_lowercase else '') + (string.digits if use_numbers else '') + (string.punctuation if use_symbols else '')
    password, used_chars = "", set()
    while len(password) < length:
        char = random.choice(characters)
        if exclude_duplicates and char in used_chars: continue
        password += char
        used_chars.add(char)
    return password
def main(stdscr):
    curses.curs_set(0); stdscr.clear()
    length, use_uppercase, use_lowercase, use_numbers, use_symbols, exclude_duplicates, password = 12, True, True, True, True, True, ""
    while 1:
        stdscr.clear()
        stdscr.addstr(0, 0, "Advanced Password Generator (Terminal UI)")
        stdscr.addstr(1, 0, "Use arrow keys to navigate, Enter to toggle options or generate password.")
        stdscr.addstr(2, 0, "Press 'q' to quit.")
        stdscr.addstr(4, 0, f"1. Password Length: {length}")
        stdscr.addstr(5, 0, f"2. Include Uppercase Letters (A-Z): {'Yes' if use_uppercase else 'No'}")
        stdscr.addstr(6, 0, f"3. Include Lowercase Letters (a-z): {'Yes' if use_lowercase else 'No'}")
        stdscr.addstr(7, 0, f"4. Include Numbers (0-9): {'Yes' if use_numbers else 'No'}")
        stdscr.addstr(8, 0, f"5. Include Symbols (@-$): {'Yes' if use_symbols else 'No'}")
        stdscr.addstr(9, 0, f"6. Exclude Duplicate Characters: {'Yes' if exclude_duplicates else 'No'}")
        stdscr.addstr(11, 0, "Generated Password: "); stdscr.addstr(12, 0, f"{password}")
        stdscr.addstr(14, 0, "Press 'g' to generate a new password with the current settings.")
        key = stdscr.getch()
        if key == ord('1'): length += 1
        elif key == ord('2'): use_uppercase = not use_uppercase
        elif key == ord('3'): use_lowercase = not use_lowercase
        elif key == ord('4'): use_numbers = not use_numbers
        elif key == ord('5'): use_symbols = not use_symbols
        elif key == ord('6'): exclude_duplicates = not exclude_duplicates
        elif key == ord('g'): password = generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols, exclude_duplicates)
        elif key == ord('q'): break
        stdscr.refresh()
curses.wrapper(main)