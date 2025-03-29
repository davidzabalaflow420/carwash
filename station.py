import threading
import time
from myqueue import Queue

class Station:
    def __init__(self, name, base_time, is_optional=False):
       
        self.name = name
        self.base_time = base_time
        self.queue = Queue()
        self.is_optional = is_optional
        self.duplicated = False  
        self.duplicate_count = 0

    def add_car(self, car):
        self.queue.enqueue(car)

   

    def has_cars(self):
        return not self.queue.is_empty()

    def reset_station(self):
        self.duplicated = False 
