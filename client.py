# Imports
import requests
import os
import time
import random

# Constants
API = "http://localhost:5000"
COLORS = {
    # Foreground Colors
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",
    # Background Colors
    "BG_BLACK": "\033[40m",
    "BG_RED": "\033[41m",
    "BG_GREEN": "\033[42m",
    "BG_YELLOW": "\033[43m",
    "BG_BLUE": "\033[44m",
    "BG_MAGENTA": "\033[45m",
    "BG_CYAN": "\033[46m",
    "BG_WHITE": "\033[47m",
    # Styles
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
}
colors = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"]


# Function: get_info(), makes connection to database/server and returns pixel count and board info
def get_info():
    request = requests.get(f"{API}/api/info")
    return request.json()


# Function: get_pixels(), makes connection to database/server and returns the pixels
def get_pixels():
    request = requests.get(f"{API}/api/pixels")
    return request.json()


# Function place_pixel(x, y, color), makes a connection to database/server and places the pixel
def place_pixel(x, y, color):
    requests.post(f"{API}/api/place", json={"x": x, "y": y, "color": color})


# Function print_name(), prints terminalPlace is ASCII art characters.
def print_name(x, y):
    # Get Current Time
    formatted_time = time.strftime("%H:%M:%S %Z")

    # Print
    print(
        r"""
  _                      _             _ _____  _                
 | |                    (_)           | |  __ \| |               
 | |_ ___ _ __ _ __ ___  _ _ __   __ _| | |__) | | __ _  ___ ___ 
 | __/ _ \ '__| '_ ` _ \| | '_ \ / _` | |  ___/| |/ _` |/ __/ _ \
 | ||  __/ |  | | | | | | | | | | (_| | | |    | | (_| | (_|  __/
  \__\___|_|  |_| |_| |_|_|_| |_|\__,_|_|_|    |_|\__,_|\___\___|

"""
        + f"{COLORS["GREEN"]} LAST UPDATED: {formatted_time} {COLORS["BOLD"]}| {COLORS["RESET"]}{COLORS["GREEN"]}GITHUB: https://github.com/sebcun/terminal-place\n{COLORS["GREEN"]} API SERVER: {API}{COLORS["BOLD"]} | {COLORS["RESET"]}{COLORS["GREEN"]}BOARD SIZE: {x}x{y}{COLORS["RESET"]}"
    )


# Function draw_board(cursor_x, cursor_y, board_width, board_height), draws the board based on info available
def draw_board(cursor_x, cursor_y, board_width, board_height):
    os.system("cls")
    print_name(board_width, board_height)
    # Top Row
    print(f"{COLORS["GREEN"]}+{"-" * board_width}+{COLORS["RESET"]}")

    # Create Main Board
    for y in range(board_height):
        row = f"{COLORS["GREEN"]}|{COLORS["RESET"]}"
        for x in range(board_width):
            if (x, y) == (cursor_x, cursor_y):
                row += "@"
            else:
                random_color = random.choice(colors)
                row += f"{COLORS[f"BG_{random_color}"]} {COLORS["RESET"]}"
        row += f"{COLORS["GREEN"]}|{COLORS["RESET"]}"
        print(row)

    # Bottom Row
    print(f"{COLORS["GREEN"]}+{"-" * board_width}+{COLORS["RESET"]}")
    print("WASD=Move | P=Place | Q=Quit")


# Function main(), starts the main logic loop
def main():
    # Get board info
    info = get_info()
    board_height = info["board_height"]
    board_width = info["board_width"]

    x, y = 0, 0

    draw_board(x, y, board_width, board_height)


# Start program
if __name__ == "__main__":
    main()
