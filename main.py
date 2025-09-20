"""
Bot for aqw
"""
import time
import random
import pyautogui
import keyboard

# 1. Simple instructions
print("Script is ready to start.")
print("Hold 'z' to start.")
print("Hold 'x' to stop.")
print("--------------------------------------------------")

# 2. A loop that waits for the start signal
while True:
    # Constantly checks if the start key is pressed
    if keyboard.is_pressed('z'):
        print("Startsignal received! Starting in 5 seconds...")
        time.sleep(5)
        break  # Breaks out of the waiting loop and continues to the main loop

# 3. The main loop that runs the automation
print("Bot is now active...")
while True:
    # Check for stop signal FIRST in each cycle
    if keyboard.is_pressed('x'):
        print("Stop signal received. Closing...")
        time.sleep(0.4)
        break  # Stops the main loop

    # Your sequence of presses
    pyautogui.press('1')
    time.sleep(random.uniform(0.2, 0.8))
    pyautogui.press('2')
    time.sleep(random.uniform(0.3, 2))
    pyautogui.press('3')
    time.sleep(random.uniform(0.3, 2))
    pyautogui.press('4')
    time.sleep(random.uniform(2, 4))
    pyautogui.press('5')
    time.sleep(random.uniform(0.3, 2))

