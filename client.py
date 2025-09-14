# Imports
import requests
import os
import time
import msvcrt
import threading
import datetime

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

# Variables
pixel_cache = []
last_fetch_time = 0.0
last_action = ""


# Function: get_info(), makes connection to database/server and returns pixel count and board info
def get_info():
    request = requests.get(f"{API}/api/info")
    return request.json()


# Function: get_pixels(), makes connection to database/server and returns the pixels
def get_pixels():
    request = requests.get(f"{API}/api/pixels")
    return request.json()


# Function fetch_pixels(), fetches pixels every 5 seconds in the background
def fetch_pixels():
    global pixel_cache, last_fetch_time
    while True:
        pixel_cache = get_pixels()
        last_fetch_time = time.time()
        time.sleep(5)


# Function place_pixel(x, y, color), makes a connection to database/server and places the pixel
def place_pixel(x, y, color):
    requests.post(f"{API}/api/place", json={"x": x, "y": y, "color": color})


# Function print_name(), prints terminalPlace is ASCII art characters.
def print_name(x, y):
    global last_fetch_time
    # Get Current Time
    dt = datetime.datetime.fromtimestamp(last_fetch_time)
    formatted_time = dt.strftime("%H:%M:%S %Z")

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
def draw_board(cursor_x, cursor_y, board_width, board_height, pixels):
    global last_action

    # Get Pixels
    pixels_dict = {(p["x"], p["y"]): p["color"] for p in pixels}

    # Clear output
    os.system("cls")
    print_name(board_width, board_height)

    # Top Row
    print(f"{COLORS["GREEN"]}+{"-" * board_width}+{COLORS["RESET"]}")

    # Create Main Board
    for y in range(board_height):

        # Create the start of the row
        row = f"{COLORS["GREEN"]}|{COLORS["RESET"]}"

        # For each item in the X
        for x in range(board_width):

            # If the cursor is in that pos, show it
            if (x, y) == (cursor_x, cursor_y):
                row += "@"
            # If the pixel is in the database show it
            elif (x, y) in pixels_dict:
                color = pixels_dict[(x, y)]
                row += f"{COLORS[f"BG_{color}"]} {COLORS["RESET"]}"
            # Otherwise blank
            else:
                row += " "

        # End of row
        row += f"{COLORS["GREEN"]}|{COLORS["RESET"]}"
        print(row)

    # Bottom Row
    print(f"{COLORS["GREEN"]}+{"-" * board_width}+{COLORS["RESET"]}")

    # Controls
    text = "WASD/Arrows = Move | P = Place | Q = Quit"
    padding = max(0, board_width - len(text))
    print(
        f"{COLORS["GREEN"]}|{COLORS['RESET']}{text}{' ' * padding}{COLORS['GREEN']}|{COLORS['RESET']}"
    )

    # Position
    text = f"Current Position: ({cursor_x}, {cursor_y})"
    padding = max(0, board_width - len(text))
    print(
        f"{COLORS["GREEN"]}|{COLORS['RESET']}{text}{' ' * padding}{COLORS['GREEN']}|{COLORS['RESET']}"
    )

    # Mid Bottom Line
    print(f"{COLORS["GREEN"]}+{"-" * board_width}+{COLORS["RESET"]}")

    # Last Action
    if last_action:
        text = last_action
        padding = max(0, board_width - len(text))
        print(
            f"{COLORS["GREEN"]}|{COLORS['RESET']}{text}{' ' * padding}{COLORS['GREEN']}|{COLORS['RESET']}"
        )
        print(f"{COLORS["GREEN"]}+{"-" * board_width}+{COLORS["RESET"]}")


# Function main(), starts the main logic loop
def main():
    global pixel_cache, last_fetch_time, last_action

    # Get board info
    info = get_info()
    board_height = info["board_height"]
    board_width = info["board_width"]

    x, y = 0, 0

    # Initial fetch
    pixel_cache = get_pixels()
    last_fetch_time = time.time()

    # Start background thread
    threading.Thread(target=fetch_pixels, daemon=True).start()

    last_draw_time = time.time()

    # While True loop (main process)
    while True:
        key_pressed = False
        key = None

        # IF a key has been pressed, fetch it and send the values
        if msvcrt.kbhit():
            key = msvcrt.getch()
            key_pressed = True

            if key == b"\xe0":
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                else:
                    key = None

        if key_pressed and key:
            # If it is an arrow
            if key == b"H" and y > 0:  # Up arrow
                y -= 1
            elif key == b"P" and y < board_height - 1:  # Down arrow
                y += 1
            elif key == b"K" and x > 0:  # Left arrow
                x -= 1
            elif key == b"M" and x < board_width - 1:  # Right arrow
                x += 1

            # Not an arrow so WASD/action
            else:
                try:
                    key_str = key.decode("utf-8").lower()
                    if key_str == "w" and y > 0:  # Up
                        y -= 1
                    elif key_str == "s" and y < board_height - 1:  # Down
                        y += 1
                    elif key_str == "a" and x > 0:  # Left
                        x -= 1
                    elif key_str == "d" and x < board_width - 1:  # Right
                        x += 1
                    elif key_str == "p":  # Place
                        color = "WHITE"
                        updated = False

                        # Adds the pixel to the pixel cache
                        for p in pixel_cache:
                            if p["x"] == x and p["y"] == y:
                                p["color"] = color
                                updated = True
                                break

                        if not updated:
                            pixel_cache.append({"x": x, "y": y, "color": color})

                        # Starts the thread for placing the pixel to the actual server
                        threading.Thread(
                            target=place_pixel, args=(x, y, color), daemon=True
                        ).start()

                        # Set the last action
                        last_action = f"Pixel placed at ({x}, {y})"
                    elif key_str == "q":  # Quit
                        break
                except UnicodeDecodeError:
                    pass

        # Update the page when a key has been pressed, OR after 5 seconds or nothing to refetch pixels
        current_time = time.time()
        if key_pressed or (current_time - last_draw_time) > 5:
            draw_board(x, y, board_width, board_height, pixel_cache)
            last_draw_time = current_time
        time.sleep(0.05)


# Start program
if __name__ == "__main__":
    main()
