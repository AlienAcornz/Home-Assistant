import time

current_timers = []

class Timer:
    def __init__(self, time_length):
        self.end_time = time.time() + time_length
        self.time_length = time_length

    def check_time(self):
        return (self.end_time - time.time()) <= 0
    
    def get_time(self):
        return self.end_time - time.time()

def set_timer(time_in_seconds):
    print(f"TIMER CREATED FOR: {time_in_seconds}")
    new_timer = Timer(time_in_seconds)
    current_timers.append(new_timer)

def get_timer(timer=False):
    print("Getting time")
    if len(current_timers) == 0:
        return False
    if timer == False:
        print("FOUND TIME LEFT")
        lowest_time_object = min(current_timers, key=lambda obj: obj.get_time())
        return lowest_time_object.get_time()
    for t in current_timers:
        if t.time_length == timer:
            print("FOUND TIME LEFT")
            return t.get_time()
        
    return False

def delete_timer(timer=False):
    print("Resetting time")
    if len(current_timers) == 0:
        return False
    if timer == False:
        print("DELETED TIMER")
        current_timers.pop(len(current_timers) - 1)
        return True
    for i, t in enumerate(current_timers):
        if t.time_length == timer:
            print("DELETED TIMER")
            current_timers.pop(i)
            return True
        
    return False