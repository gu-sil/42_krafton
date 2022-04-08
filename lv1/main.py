"""Simple example showing how to get keyboard events."""

import inputs
import os
import datetime
import time
import threading
from scene_manager import SceneManager

running = True

key_states = {}
cached_key_states = {}
dcached_key_states = {}

class KBThread (threading.Thread):
    def run(self):
        global key_states
        global running
        while running:
            try:
                events = inputs.get_key()
                for event in events:
                    key_states[event.code] = event.state
            except:
                pass

class KBManager:
    def __init__(self):
        global key_states
        global cached_key_states
        global dcached_key_states
        key_states = {}
        cached_key_states = {}
        dcached_key_states = {}
        self._last_key_time = {}
        self._double_key_tolerance = 1.0

    def clean_key_states(self):
        global key_states
        global cached_key_states
        global dcached_key_states

        dcached_key_states = cached_key_states
        cached_key_states = key_states
        key_states = {}
        for key in cached_key_states.keys():
            if cached_key_states[key] == 1:
                key_states[key] = 1

    def update_last_key_time(self, keycode: str, update_time: datetime):
        self._last_key_time[keycode] = update_time

    def get_key_pressed(self, keycode: str):
        global key_states

        # 이 프레임에 해당 키가 릴리즈됐을 경우
        if  keycode in key_states and \
            key_states[keycode] == 0:
            return True
        else:
            return False

    # 이전과 현재 프레임에 키가 눌러져있다면 True 반환
    def get_key_pressing(self, keycode: str):
        global key_states

        if  keycode in cached_key_states and cached_key_states[keycode] == 1 and \
            keycode in key_states and key_states[keycode] == 1:
            return True
        else:
            return False

    def get_double_key_down(self, keycode: str):
        global key_states
        global cached_key_states

        # 일정시간 안에 키가 눌려졌을 경우
        if  keycode not in self._last_key_time:
            return False
        elif  keycode in cached_key_states and cached_key_states[keycode] == 1 and \
            keycode in key_states and key_states[keycode] == 0:
            key_interval = datetime.datetime.now() - self._last_key_time[keycode]
            if key_interval.total_seconds() <= self._double_key_tolerance:
                return True
            else:
                return False
        else:
            return False

def process_keyboard_input(sm : SceneManager, kb : KBManager):
    if kb.get_key_pressed("KEY_UP") and kb.get_key_pressing("KEY_LEFTSHIFT"):
        sm.add_movement_input(0, 2)
        kb.update_last_key_time("KEY_UP", datetime.datetime.now())
    elif kb.get_double_key_down("KEY_UP"):
        sm.add_movement_input(0, 2)
        kb.update_last_key_time("KEY_UP", datetime.datetime.now())
    elif kb.get_key_pressed("KEY_UP"):
        sm.add_movement_input(0, 1)
        kb.update_last_key_time("KEY_UP", datetime.datetime.now())

    if kb.get_key_pressed("KEY_LEFT") and kb.get_key_pressing("KEY_LEFTSHIFT"):
        sm.add_movement_input(-2, 0)
        kb.update_last_key_time("KEY_LEFT", datetime.datetime.now())
    elif kb.get_double_key_down("KEY_LEFT"):
        sm.add_movement_input(-2, 0)
        kb.update_last_key_time("KEY_LEFT", datetime.datetime.now())
    elif kb.get_key_pressed("KEY_LEFT"):
        sm.add_movement_input(-1, 0)
        kb.update_last_key_time("KEY_LEFT", datetime.datetime.now())

    if kb.get_key_pressed("KEY_DOWN") and kb.get_key_pressing("KEY_LEFTSHIFT"):
        sm.add_movement_input(0, -2)
        kb.update_last_key_time("KEY_DOWN", datetime.datetime.now())
    elif kb.get_double_key_down("KEY_DOWN"):
        sm.add_movement_input(0, -2)
        kb.update_last_key_time("KEY_DOWN", datetime.datetime.now())
    elif kb.get_key_pressed("KEY_DOWN"):
        sm.add_movement_input(0, -1)
        kb.update_last_key_time("KEY_DOWN", datetime.datetime.now())

    if kb.get_key_pressed("KEY_RIGHT") and kb.get_key_pressing("KEY_LEFTSHIFT"):
        sm.add_movement_input(2, 0)
        kb.update_last_key_time("KEY_RIGHT", datetime.datetime.now())
    elif kb.get_double_key_down("KEY_RIGHT"):
        sm.add_movement_input(2, 0)
        kb.update_last_key_time("KEY_RIGHT", datetime.datetime.now())
    elif kb.get_key_pressed("KEY_RIGHT"):
        sm.add_movement_input(1, 0)
        kb.update_last_key_time("KEY_RIGHT", datetime.datetime.now())

    if kb.get_key_pressed("KEY_ESC"):
        global running
        running = False

def update(sm : SceneManager, kb : KBManager):
    # deal with input
    process_keyboard_input(sm, kb)
    # render
    sm.render()
    # clean keyboard states
    kb.clean_key_states()

# MAIN LOOP
def main():

    # init()
    sm = SceneManager(40, 20, "./s1.rl")
    kb = KBManager()
    last_update_time = datetime.datetime.fromtimestamp(time.mktime(time.gmtime()))

    t = KBThread()
    t.daemon = True
    t.start()

    global running
    while running:
        current_time = datetime.datetime.now()
        delta_time = current_time - last_update_time;

        if (delta_time.total_seconds()) >= 0.1:
            update(sm, kb)
            last_update_time = current_time

    inputs.devices.keyboards[0]._listener.terminate()
    print("bye~")
    t.join()
    os._exit(0)

if __name__ == "__main__":
    main()
