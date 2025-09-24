import time
import random
import threading
import pygetwindow as gw
import win32gui
import win32api
import win32con
import keyboard
import numpy as np
import cv2 as cv
import pyautogui
import PIL

# --- Configuration ---
GAME_WINDOW_TITLE = 'Artix Game Launcher'  # The exact title of your game window

ABILITY_TYPES = {}

KEY_CODES = {
    1: 0x31,
    2: 0x32,
    3: 0x33,
    4: 0x34,
    5: 0x35
}


# --- Helper Functions ---
def press_key(hwnd, key_code):
    """Sends a KEYDOWN and KEYUP message to the specified window handle."""
    # Send the key down message
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key_code, 0)
    # Wait a tiny, random amount of time
    time.sleep(random.uniform(0.05, 0.1))
    # Send the key up message
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key_code, 0)
 

   


def capture_game_screen(hwnd):
    """Captures the game window screen and returns it as a Pillow Image object."""
    try:
        # Get window position and size
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        
        # Capture using pyautogui - this is already a Pillow Image object
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        return screenshot  # <-- Return the original Pillow Image
    except Exception as e:
        print(f"Screenshot capture failed: {e}")
        return None



def map_abilities(): # No need to pass arguments
    """Allows user to map their abilities as health or attack skills."""
    global ABILITY_TYPES
    print("\n=== ABILITY MAPPING ===")
    print("Map your abilities as Health or Attack skills.")
    
    for i in range(1, 6): # This will loop for skills 1, 2, 3, 4, 5
        while True:
            user_input = input(f"Is your skill '{i}' a Health or Attack skill? (h/a): ").lower().strip()
            if user_input == 'h':
                ABILITY_TYPES[i] = 'health'
                print(f"-> Skill {i} set as Health.")
                break
            elif user_input == 'a':
                ABILITY_TYPES[i] = 'attack'
                print(f"-> Skill {i} set as Attack.")
                break
            else:
                print("Invalid input. Please enter 'h' or 'a'.")
    
    print("\nAbility mapping complete!")
    print("Current mapping:")
    for skill_num, skill_type in ABILITY_TYPES.items():
        print(f"  Skill {skill_num}: {skill_type.title()}")
    print()

def run_bot_logic(hwnd, game_window):
    """
    Contains the main loop for the bot's actions, with a clean,
    updating status line and a randomized skill order.
    """
    global stop_thread
    while not stop_thread:
        # Check if the user has mapped any abilities
        if ABILITY_TYPES:
            # --- SMART ROTATION (ABILITIES ARE MAPPED) ---
            
            # 1. Get the list of mapped skills as a list
            mapped_skills = list(ABILITY_TYPES.items())
            # 2. Shuffle the list to randomize the order! 
            random.shuffle(mapped_skills)

            for skill_number, skill_type in mapped_skills:
                if stop_thread: break

                status_text = f"[Mapped Rotation] Using {skill_type.title()} Skill {skill_number}..."
                print(f"{status_text.ljust(70)}", end='\r')
                press_key(hwnd, KEY_CODES[skill_number])
                
                cooldown = random.uniform(0.02, 0.4)
                time.sleep(cooldown)
        
        else:
            # --- DEFAULT ROTATION (NO MAPPING DONE) ---
            default_skills = [1, 2, 3, 4, 5]
            # Shuffle the list of default skills to randomize the order! ✅
            random.shuffle(default_skills)

            for skill_number in default_skills:
                if stop_thread: break

                status_text = f"[Default Rotation] Using Skill {skill_number}..."
                print(f"{status_text.ljust(70)}", end='\r')
                press_key(hwnd, KEY_CODES[skill_number])
                time.sleep(random.uniform(0.02, 0.4))

        # After a full rotation, show an idle status
        idle_status = "[Rotation Complete] Waiting for next cycle..."
        print(f"{idle_status.ljust(70)}", end='\r')
        time.sleep(random.uniform(0.1, 0.5))

    # When the loop is stopped, clear the status line
    print(" " * 70, end='\r')

           
# --- Main Script Logic ---

# 1. Find the game window dynamically
try:
    game_window = gw.getWindowsWithTitle(GAME_WINDOW_TITLE)[0]
    hwnd = game_window._hWnd
    print(f"'{GAME_WINDOW_TITLE}' window found with handle: {hwnd}")
except IndexError:
    print(f"Error: '{GAME_WINDOW_TITLE}' window not found. Please start the game.")
    exit()

# 2. The main "menu" loop that the program will always return to
while True:
    # 3. Print the main menu options
    print("\n--- Bot Main Menu ---")
    print("Hold 'z' -> START the bot")
    print("Hold 'm' -> MAP abilities")
    print("---------------------")
    # Show the current status
    if ABILITY_TYPES:
        print("INFO: Custom ability map is active.")
    else:
        print("INFO: No custom map. Bot will use default rotation.")

    # 4. Wait for the user to choose an action ('z' or 'm')
    action = None
    while True:
        if keyboard.is_pressed('z'):
            action = 'start'
            break
        if keyboard.is_pressed('m'):
            action = 'map'
            break
        time.sleep(0.05) # Prevents high CPU usage

    # 5. Execute the chosen action
    if action == 'map':
        ABILITY_TYPES.clear() # Clear old settings before mapping new ones
        map_abilities()
        # After mapping is done, 'continue' tells the loop to start over,
        # which will reprint the main menu.
        continue

    elif action == 'start':
        # This block runs the bot
        print("\nBot is now active...")
        print("Hold 'q' to hide, 'y' to show, 'x' to STOP.")
        
        stop_thread = False
        bot_thread = threading.Thread(target=run_bot_logic, args=(hwnd, game_window), daemon=True)
        bot_thread.start()

        # Inner loop for hotkeys while the bot is running
        while True:
            if keyboard.is_pressed('x'):
                print("\nStop key pressed. Stopping bot and returning to main menu...")
                stop_thread = True
                bot_thread.join()
                game_window.moveTo(100, 100)
                game_window.activate()
                # 'break' exits this inner loop and returns to the main menu loop
                break

            if keyboard.is_pressed('q'):
                print("Hiding window...")
                game_window.moveTo(-2000, 0)
                time.sleep(0.5)

            if keyboard.is_pressed('y'):
                print("Showing window...")
                game_window.moveTo(100, 100)
                game_window.activate()
                time.sleep(0.5)
            
            time.sleep(0.1)
        
