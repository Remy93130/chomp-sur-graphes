"""Module for manage the time in the game"""

# Imports ---------------------------------------------------------------------

from threading import Thread, Event
import time

# Classes ---------------------------------------------------------------------

class Timer(Thread):
    """Class for create a coutdown during the game"""
    def __init__(self, max_time, end_of_thread):
        Thread.__init__(self)
        self.max_time = max_time
        self.end_of_thread = end_of_thread

    def run(self):
        """Method for run the thread when the thread is
        over the attribute end_of_thread is set"""
        while self.max_time != 0:
            time.sleep(1)
            self.max_time -= 1
        self.end_of_thread.set()

def main():
    """Main for test the class"""
    end_of_thread = Event()
    end_of_thread.clear()
    time_begin = time.time()
    timer = Timer(5, end_of_thread)
    timer.start()
    print('START')
    while not end_of_thread.is_set():
        print("\tProcessing...\n\tmax_time = {}".format(timer.max_time))
        time.sleep(.5)
    print("FINISH")
    print("Total execution time : {} seconds".format(time.time() - time_begin))

if __name__ == '__main__':
    main()
