import webview
import threading
import psutil
import time
import sys
import os
from app import app

# Add the process names of the applications you want to lock (must include .exe)
# Example: LOCKED_APPS = ["chrome.exe", "spotify.exe", "discord.exe"]
LOCKED_APPS = [""]

def get_config_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), "config.txt")
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")

class Api:
    def __init__(self):
        self._window = None
        self.authenticated = False

    def set_window(self, window):
        self._window = window

    def unlock_system(self):
        print("Access Granted - Hiding window")
        self.authenticated = True 
        if self._window:
            self._window.hide()

    def save_rating(self, rating):
        try:
            with open(get_config_path(), "w") as f:
                f.write(str(rating))
        except Exception as e:
            print(f"Error saving rating: {e}")

    def get_saved_rating(self):
        path = get_config_path()
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return f.read().strip()
            except:
                pass
        return "1600"

def on_closing():
    if api.authenticated:
        return True
    
    print("The puzzle must be solved to gain access.")
    return False

def monitor_processes(window, api):
    chrome_was_running = False

    while True:
        try:
            chrome_is_running = any(p.info['name'].lower() in [app.lower() for app in LOCKED_APPS] 
                                    for p in psutil.process_iter(['name']))
            
            if chrome_is_running:
                if not api.authenticated:
                    window.show()
                    window.restore()
                chrome_was_running = True
            else:
                if chrome_was_running:
                    print("Chrome closed.")
                    api.authenticated = False
                    window.hide()
                    window.load_url(f'http://127.0.0.1:5000?t={int(time.time())}')
                    chrome_was_running = False

        except Exception as e:
            print(f"Monitor error: {e}")
        
        time.sleep(1)

def start_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    api = Api()

    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    window = webview.create_window(
        'Zugzwang Security', 
        'http://127.0.0.1:5000',
        js_api=api,
        width=500, height=750,
        on_top=True, frameless=True, easy_drag=False,
        hidden=True
    )
    
    api.set_window(window)
    window.events.closing += on_closing
    
    monitor_thread = threading.Thread(target=monitor_processes, args=(window, api))
    monitor_thread.daemon = True
    monitor_thread.start()

    webview.start()