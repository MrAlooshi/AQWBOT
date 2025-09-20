import time
import random
import pygetwindow as gw
import win32gui
import win32api
import win32con
import keyboard

print(gw.getAllTitles())
# --- Configuration ---
GAME_WINDOW_TITLE = 'Artix Game Launcher'  # The exact title of your game window

# --- Helper Function ---
def press_key(hwnd, key_code):
    """Sends a KEYDOWN and KEYUP message to the specified window handle."""
    # Send the key down message
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key_code, 0)
    # Wait a tiny, random amount of time
    time.sleep(random.uniform(0.05, 0.1))
    # Send the key up message
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key_code, 0)

# --- Main Script Logic ---

# 1. Find the game window dynamically
try:
    game_window = gw.getWindowsWithTitle(GAME_WINDOW_TITLE)[0]
    hwnd = game_window._hWnd  # Get the handle for win32 functions
    print(f"'{GAME_WINDOW_TITLE}' window found with handle: {hwnd}")
except IndexError:
    print(f"Error: '{GAME_WINDOW_TITLE}' window not found. Please start the game.")
    exit()  # Stop the script if the window doesn't exist

# 2. Wait for the user to start the bot
print("\nBot is ready. Hold 'z' to start, hold 'x' to stop.")
print("Press 'q' to hide the game window, 'y' to show the game window")
keyboard.wait('z')

# 3. Main bot loop
print("Bot is now active...")
while True:
    # Check for the stop key first
    if keyboard.is_pressed('x'):
        print("Stop key pressed. Exiting.")
        break
    
    if keyboard.is_pressed('q'):
        print("Hiding window...")
        game_window.moveTo(-2000, 0) # Move it off-screen
        time.sleep(0.5)

    if keyboard.is_pressed('y'):
        print("Showing window...")
        game_window.moveTo(100, 100) # Move it back to the top-left
        game_window.activate()
        time.sleep(0.5) # A small pause

    # Perform the action sequence
    print("Running combat rotation...")
    press_key(hwnd, 0x31) # '1' key
    time.sleep(random.uniform(0.1, 0.3))
    
    press_key(hwnd, 0x32) # '2' key
    time.sleep(random.uniform(0.2, 0.4))

    press_key(hwnd, 0x33) # '3' key
    time.sleep(random.uniform(0.2, 0.8))

    press_key(hwnd, 0x34) # '4' key
    time.sleep(random.uniform(1, 3))

    press_key(hwnd, 0x35) # '5' key
    time.sleep(random.uniform(0.5, 1.2))

print("\nBot has been stopped.")