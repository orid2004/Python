import time
import math
import datetime


class Timer:
    # --- Timer object ---
    def __init__(self):
        self.start_time = None
        self.on = False

    def start(self):
        # start counting
        self.start_time = time.time()
        self.on = True

    def value(self):
        # --- return current value ---
        if self.on:
            return time.time() - self.start_time
        else:
            return 0

    def tostr(self):
        # --- return value as {min:sec} format ---
        val = math.floor(self.value())
        min = '0' + str(int(val / 60)) if len(str(int(val / 60))) == 1 else str(int(val / 60))
        sec = '0' + str(val % 60) if len(str(val % 60)) == 1 else str(val % 60)
        return "{}:{}".format(min, sec)

    def stop(self):
        # --- stop counting ---
        self.__init__()


def best_time(*args) -> str:
    # --- compare and return best of datetimes ---
    # --- compares only {min:sec} format
    best = datetime.datetime(1, 1, 1, 1, 0, 0)
    for s_time in args:
        # --- update best ---
        dt = datetime.datetime(1, 1, 1, 1, int(s_time.split(':')[0]), int(s_time.split(':')[1]))
        best = dt if dt > best else best
    # --- convert to format --
    best = [str(best.minute), str(best.second)]
    for i in [0, 1]:
        if len(best[i]) == 1:
            best[i] = '0' + best[i]  # --- add zeros ---
    # --- return as string ---
    return "{}:{}".format(*best)
