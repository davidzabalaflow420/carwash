from stack import Stack
from station import Station

class StationController:
    
    def __init__(self, station_manager):
        self.station_manager = station_manager

    def process_cars(self):
        if self.station_manager.get_stations().size() == 0:
            print("❌ No hay estaciones disponibles.")
            return
        
        for station in self.station_manager.get_stations().items:
            if station.has_cars():
                print(f"🚗 Procesando autos en {station.name}...")
                station.process_car()

    def advance_cars(self):
        self.handle_congestion()
        self.reorder_stations()
        self.process_advanced_cars()

    def handle_congestion(self):
        temp_stack = Stack()

        while not self.station_manager.stations.is_empty():
            station = self.station_manager.stations.pop()
            if station.queue.size() > 5:
                print(f"⚠️ Alerta: Congestión en {station.name} ({station.queue.size()} autos). Duplicando estación.")
                self.create_and_redistribute_duplicate_station(station, temp_stack)

            temp_stack.push(station)

    def create_and_redistribute_duplicate_station(self, station, temp_stack):
        duplicate = self.create_duplicate_station(station)
        half_size = station.queue.size() // 2
        for _ in range(half_size):
            duplicate.queue.enqueue(station.queue.dequeue())
        temp_stack.push(duplicate)

    def create_duplicate_station(self, station):
        return Station(f"{station.name}-2", station.base_time, station.is_optional)

    def reorder_stations(self):
        aux_stack = Stack()
        while not self.station_manager.stations.is_empty():
            station = self.station_manager.stations.pop()
            aux_stack.push(station)

        while not aux_stack.is_empty():
            self.station_manager.stations.push(aux_stack.pop())

    def process_advanced_cars(self):
        temp_stack = Stack()

        while not self.station_manager.stations.is_empty():
            station = self.station_manager.stations.pop()
            print(f"🔧 Procesando estación {station.name}...")

            next_station = None if temp_stack.is_empty() else temp_stack.peek()

            self.move_cars_to_next_station(station, next_station)
            temp_stack.push(station)

        while not temp_stack.is_empty():
            self.station_manager.stations.push(temp_stack.pop())

    def move_cars_to_next_station(self, station, next_station):
        while station.has_cars():
            car = station.queue.first()
            if next_station and next_station.queue.size() < 5:
                station.queue.dequeue()
                next_station.queue.enqueue(car)
            else:
                break

