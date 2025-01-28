import sys
import tty
import os
import termios
from time import sleep
import json

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def cli_select(options):
    selection = 0
    while True:
        os.system("clear")
        for i, option in enumerate(options):
            print(f"\033[92m  {'>' if i == selection else ' '}\033[0m {option}")
        char = get_char()
        if char == 'A':
            selection = (selection - 1) % len(options)
        elif char == 'B':
            selection = (selection + 1) % len(options)
        elif char == '\r':
            return options[selection]

if __name__ == '__main__':
    with open("models.json") as f:
        options = list(json.load(f).keys())

    selected = cli_select(options)
    os.system("clear")
    print(f"Selected: {selected}")
    with open("temp/model_name.tmp", "w") as f:
        f.write(selected)
    os.system("uvicorn app:app --reload --host 0.0.0.0 --port 8000")

