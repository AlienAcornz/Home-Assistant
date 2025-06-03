import time

current_timers = []

class Timer:
    def __init__(self, time_length):
        self.end_time = time.time + time_length
        self.start_time = time.time()
        self.time_length = time_length

    def check_time(self):
        return (self.end_time - self.start_time) <= 0

def set_timer(time_in_seconds):
    new_timer = Timer(time_in_seconds)
    current_timers.append(new_timer)

def get_timer(timer=False):
    if len(current_timers) == 0:
        return False
    if timer == False:
        return current_timers[len(current_timers) - 1].time_length
    for t in current_timers:
        local_time_length = t.time_length
        if local_time_length == timer:
            return local_time_length
        
    return False

def reset_timer(timer=False):
    if len(current_timers) == 0:
        return False
    if timer == False:
        current_timers.pop(len(current_timers) - 1)
        return True
    for i, t in enumerate(current_timers):
        local_time_length = t.time_length
        if local_time_length == timer:
            current_timers.pop(i)
            return True
        
    return False