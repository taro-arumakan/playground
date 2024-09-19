import os
import time
import pyautogui
import pyperclip

def send():
    # Get text from the clipboard
    clipboard_text = pyperclip.paste()

    def activate_app(app_name):
        os.system(f"""osascript -e 'activate application "{app_name}"'""")

    # Activate the TextEdit application
    activate_app('VMWare Horizon Client')

    # Give time to activate
    time.sleep(0.5)

    # Send keystrokes to the application. Default interval=0.0
    pyautogui.typewrite(clipboard_text)
    pyautogui.press('enter')

