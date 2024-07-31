import time
import logging
import keyboard

class HotkeyListener:
    def __init__(self, callback):
        self.callback = callback
        self.first_time = 0

    def start(self):
        keyboard.add_hotkey('ctrl+c', self.on_ctrl_c_double)

    def on_ctrl_c_double(self):
        current_time = time.time()
        if current_time - self.first_time < 0.5:
            logging.info(f"Ctrl+C pressed at {current_time}")
            self.callback()
        self.first_time = current_time

    def stop(self):
        keyboard.unhook_all()
