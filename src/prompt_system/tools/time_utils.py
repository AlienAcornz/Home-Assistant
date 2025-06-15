import time
import threading
from pathlib import Path
import pygame
from ...api_system.log_utils import add_log

current_timers = []
ALARM_PATH = Path(__file__).resolve().parents[3] / "assets" / "star-destroyer-alarm.wav"
class Timer:
    def __init__(self, time_length):
        self.end_time = time.time() + time_length
        self.time_length = time_length

    def check_time(self):
        return (self.end_time - time.time()) <= 0
    
    def get_time(self):
        return self.end_time - time.time()

def set_timer(time_in_seconds):
    add_log(f"Timer created for {time_in_seconds}s", tag="tools")
    print(f"TIMER CREATED FOR: {time_in_seconds}")
    new_timer = Timer(time_in_seconds)
    current_timers.append(new_timer)

def get_timer(timer=False):
    add_log(f"Getting time for {timer} timer", tag="tools") if timer else add_log(f"Getting timer for most recent timer", tag="tools")
    if len(current_timers) == 0:
        return False
    if timer == False:
        lowest_time_object = min(current_timers, key=lambda obj: obj.get_time())
        add_log(f"Timer has {lowest_time_object.get_time()}s left", "tools")
        return lowest_time_object.get_time()
    for t in current_timers:
        if t.time_length == timer:
            print("FOUND TIME LEFT")
            return t.get_time()
        
    return False

def delete_timer(timer=False):
    add_log(f"Deleting timer for {timer}s", tag="tools") if timer else add_log(f"Deleting most recent timer", tag="tools")
    if len(current_timers) == 0:
        return False
    if timer == False:
        add_log("Timer deleted!", tag="tools")
        current_timers.pop(len(current_timers) - 1)
        return True
    for i, t in enumerate(current_timers):
        if t.time_length == timer:
            add_log("Timer deleted!", tag="tools")
            current_timers.pop(i)
            return True
        
    return False

active_alarm = False

__stop_event = threading.Event()
__alarm_thread = None

def __play_alarm():
    global active_alarm
    if active_alarm:
        add_log("Tried to create an alarm whilst another alarm is going off.", tag="error")
        return -1

    __set_active_state(True)
    pygame.mixer.init()
    pygame.mixer.music.load(ALARM_PATH)
    pygame.mixer.music.play(-1)
    while not __stop_event.is_set():
        time.sleep(0.1)
    pygame.mixer.music.stop()
    __stop_event.clear()

def start_alarm():
    add_log("Alarm started!", tag="tools")
    global __alarm_thread
    if __alarm_thread is None or not __alarm_thread.is_alive():
        __alarm_thread = threading.Thread(target=__play_alarm)
        __alarm_thread.start()

def stop_alarm():
    __set_active_state(False)
    add_log("Alarm stopped!", tag="tools")
    print("alarm stopped")
    __stop_event.set()

def check_alarm():
    for timer in current_timers[:]:
        if timer.check_time() == True:
            current_timers.remove(timer)
            __play_alarm()
            break

def __set_active_state(state: bool):
    global active_alarm
    active_alarm = state

def get_active_state():
    global active_alarm
    return active_alarm