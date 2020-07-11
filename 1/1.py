import os
import time
import pyautogui

print(pyautogui.position() )
time.sleep(2)
print(pyautogui.size())

# pyautogui.moveTo(100, 220)  # move mouse to XY coordinates over num_second seconds
pyautogui.click(x=100, y=220, clicks=2, interval=0.2, button='left')
