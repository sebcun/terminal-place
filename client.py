# Imports
import requests
import colorama
from colorama import Fore, Back, Style
import os
import time

# Constants
API = "http://localhost:5000"


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
        + Fore.GREEN
        + f"LAST UPDATED: {formatted_time}"
        + Style.DIM
        + " | "
        + Style.NORMAL
        + "GITHUB: https://github.com/sebcun/terminal-place\n"
        + f"API SERVER: {API}"
        + Style.DIM
        + " | "
        + Style.NORMAL
        + f"BOARD SIZE: {x} x {y}"
    )


# Function draw_board(cursor_x, cursor_y, board_width, board_height), draws the board based on info available
def draw_board(cursor_x, cursor_y, board_width, board_height):
    os.system("cls")
    print_name(board_width, board_height)
    # Top Row
    print(Style.BRIGHT + "+" + "-" * board_width + "+")

    # Create Main Board
    for y in range(board_height):
        row = "|"
        for x in range(board_width):
            row += " "
        row += "|"
        print(row)

    # Bottom Row
    print("+" + "-" * board_width + "+")
    print(Fore.RESET + "WASD=Move | P=Place | Q=Quit")


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
