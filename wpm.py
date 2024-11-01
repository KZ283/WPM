import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to my game!")
    stdscr.addstr("\nPress any key to begin.")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(10, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)

        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def load_text():
    with open("Test.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text = load_text()
    custom_text = []
    wpm = 0
    start_time = time.time()  # no of seconds passed
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(custom_text) / (time_elapsed/60))/5)   #assuming every word is of 5 chars

        stdscr.clear()

        display_text(stdscr, target_text, custom_text, wpm)

        stdscr.refresh()

        if "".join(custom_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # esc key
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(custom_text) > 0:
                custom_text.pop()
        elif len(custom_text) < len(target_text):
            custom_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(11, 0, "You completed the game! Press any key to continue...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)
