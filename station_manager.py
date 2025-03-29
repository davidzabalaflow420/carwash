from stack import Stack
from station import Station
from myqueue import Queue
from station_controller import StationController
from data_persistence import DataPersistence
from redistribute import Redistribute

class StationManager:
    
    MAX_DUPLICATIONS = 3  

    def __init__(self, setup_default=True):
        
        self.stations = Stack()
        if setup_default:
        
            self.setup_stations()

    def setup_stations(self):
        self.add_station("Secado", 3, is_optional=True)
        self.add_station("Enjuague", 4)
        self.add_station("Enjabonado", 5)
        self.add_station("Prelavado", 3, is_optional=True)

    def add_station(self, name, base_time, is_optional=False):
        self.stations.push(Station(name, base_time, is_optional))

    def remove_station_by_name(self, station_name):
        self.stations.items = [station for station in self.stations.items if station.name.lower() != station_name.lower()]

    def remove_station(self, station_name):
        removed_station = next((st for st in self.stations.items if st.name.lower() == station_name.lower()), None)
        
        if removed_station:
            self.remove_station_by_name(station_name)  
            redistribute = Redistribute(self)
            redistribute.redistribute_cars(removed_station)

        return removed_station

    def toggle_drying(self, enable):
        if enable:
            if not any(station.name.lower() == "secado" for station in self.stations.items):
                self.stations.push(Station("Secado", 3, is_optional=True))
        else:
            self.remove_station_by_name("Secado")  

    def assign_car_to_station(self, car):
        if not self.stations.is_empty():
            congested_stations = [station for station in self.stations.items if station.queue.size() > 5]
            for station in congested_stations:
                print(f"⚠️ Alerta: Congestión en la estación {station.name}, duplicando estación.")
                self.duplicate_station(station)
            
            print(f"🚗 Agregando auto {car.license_plate} a la estación {self.stations.peek().name}")
            self.stations.peek().add_car(car)

    def duplicate_station(self, station):
        if station.duplicate_count >= self.MAX_DUPLICATIONS: 
            print(f"No se puede duplicar más la estación {station.name}. Límite alcanzado.")
            return

        duplicate_station = Station(f"{station.name}-2", station.base_time, station.is_optional)  
        duplicate_station.duplicate_count = station.duplicate_count + 1  

        queue_half = [station.queue.dequeue() for _ in range(station.queue.size() // 2)]
        for car in queue_half:
            duplicate_station.add_car(car)

        self.stations.push(duplicate_station)
        print(f"Estación duplicada creada: {duplicate_station.name}")

    def load_from_state(self, saved_state):
        self.stations = Stack()
        for station_data in saved_state["stations"]:
            name, base_time, is_optional = station_data["name"], station_data["base_time"], station_data["is_optional"]
            self.add_station(name, base_time, is_optional)

    def get_stations_data(self):
        return [{"name": station.name, "base_time": station.base_time, "is_optional": station.is_optional} for station in self.stations.items]

    def get_stations(self):
        return self.stations

    def __str__(self):
        return " -> ".join(station.name for station in self.stations.items) if not self.stations.is_empty() else "No hay estaciones disponibles."