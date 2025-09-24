import cv2 as cv
import numpy as np
import pyautogui
import time

# --- Instructions ---
print("The screen will be captured in 3 seconds...")
print("After the image appears, click on the color you want to analyze.")
print("Press any key to close the image window when you're done.")
print("--------------------------------------------------")

time.sleep(3)

# Take a screenshot
screenshot = pyautogui.screenshot()
screenshot_cv = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

# This function will be called when you click the mouse
def get_pixel_color(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Get the BGR color of the clicked pixel
        pixel_bgr = screenshot_cv[y, x]
        
        # Convert BGR to HSV
        pixel_hsv = cv.cvtColor(np.uint8([[pixel_bgr]]), cv.COLOR_BGR2HSV)[0][0]
        
        print(f"You clicked on pixel ({x}, {y})")
        print(f"BGR Color: {pixel_bgr}")
        print(f"HSV Color: [Hue={pixel_hsv[0]}, Saturation={pixel_hsv[1]}, Value={pixel_hsv[2]}]")
        print("---")

# Create a window to display the screenshot
cv.namedWindow('Color Picker - Click on a color')
cv.setMouseCallback('Color Picker - Click on a color', get_pixel_color)

# Show the screenshot and wait for user interaction
cv.imshow('Color Picker - Click on a color', screenshot_cv)
cv.waitKey(0)
cv.destroyAllWindows()