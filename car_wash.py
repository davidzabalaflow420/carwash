import threading
import time
from myqueue import Queue
from station_manager import StationManager
from stack import Stack
from station_controller import StationController
from data_persistence import DataPersistence
from car import Car

class CarWashSystem:
    def __init__(self):
        self.filepath = "car_wash_state.json"  
        self.station_manager = StationManager()
        self.car_queue = Queue()
        self.station_controller = StationController(self.station_manager)
        self.deleted_stations = []
        
        self.load_state()

    def load_state(self):
        saved_state = DataPersistence.load_state(self.filepath)
        if saved_state:
            self.station_manager.load_from_state(saved_state)
            for car_data in saved_state.get("cars", []):
                car_type, plate, is_express, skip_stations = car_data
                self.car_queue.enqueue(Car(car_type, plate, is_express, skip_stations))
            self.deleted_stations = saved_state.get("deleted_stations", [])

    def add_car(self, plate, car_type, express=False, skip_stations=None): 
        self.car_queue.enqueue(Car(car_type, plate, express, skip_stations))
        self.save_state()

    def process_cars(self):
        if self.car_queue.is_empty():
            print("🚗 No hay autos en la cola para procesar.")
            return

        threads = []
        while not self.car_queue.is_empty():
            car = self.car_queue.dequeue()
            for station in self.station_manager.get_stations().items:
                if station.name not in car.skip_stations:
                    t = threading.Thread(target=self.process_car_in_station, args=(car, station))
                    threads.append(t)
                    t.start()
        for t in threads:
            t.join()

        print("Todos los autos han sido procesados.")
        self.save_state()

    def process_car_in_station(self, car, station):
        print(f"{car} ingresó a {station.name}. [Hilo: {threading.current_thread().name}]")

        processing_time = car.get_processing_time(station.base_time)
        print(f"Procesando {car} en {station.name} por {processing_time} segundos... [Hilo: {threading.current_thread().name}]")
        
        time.sleep(processing_time)
       
        print(f"{car} ha terminado en {station.name}.[Hilo: {threading.current_thread().name}]")
        
        car.processed_station = station.name
        self.move_car_to_next_station(car)

    def move_car_to_next_station(self, car):
        stations = self.station_manager.get_stations().items
        for i, station in enumerate(stations):
            if station.name == car.processed_station and i + 1 < len(stations):
                next_station = stations[i + 1]
                if next_station.queue.size() < 5:
                    self.station_manager.assign_car_to_station(car)
                else:
                    station.add_car(car)
                break

    def toggle_drying(self, enable):
        self.station_manager.toggle_drying(enable)
        self.save_state()
        estado = "activado" if enable else "desactivado"
        print(f"💨 Secado {estado}.")

    def add_station(self, name, base_time, is_optional=False):
        self.station_manager.add_station(name, base_time, is_optional)
        self.save_state()
        print(f"🏗️ Estación '{name}' agregada con éxito.")

    def remove_station(self, station_name):
        removed_station = self.station_manager.remove_station(station_name)
        if removed_station:
            self.deleted_stations.append({
                'name': removed_station.name,
                'base_time': removed_station.base_time,
                'is_optional': removed_station.is_optional
            })
            self.save_state()
            print(f"🚫 Estación '{station_name}' eliminada con éxito.")
        else:
            print(f"⚠️ No se encontró la estación '{station_name}'.")

    def restore_deleted_stations(self):
        if not self.deleted_stations:
            print("⚠️ No hay estaciones eliminadas para restaurar.")
            return

        for station_data in self.deleted_stations: 
            self.station_manager.add_station(station_data['name'], station_data['base_time'], station_data['is_optional'])
            print(f"🔄 Estación '{station_data['name']}' restaurada con éxito.")

        self.deleted_stations.clear()
        self.save_state()

    def get_status(self):
        status = "🚘 Estado del Sistema de Lavado de Autos:\n"
        estaciones = " -> ".join(station.name for station in reversed(self.station_manager.get_stations().items))
        status += f"🏭 Estaciones activas: {estaciones if estaciones else 'No hay estaciones disponibles.'}\n"

        if self.car_queue.size() == 0:
            status += "🚗 No hay autos en la cola.\n"
        else:
            autos = ", ".join(str(car) for car in self.car_queue.get_items())  
            status += f"🚗 Autos en espera: {autos}\n"

        return status
    


    
    def get_cars_data(self):
     return [(car.car_type, car.license_plate, car.is_express, car.skip_stations) for car in self.car_queue.get_items()]


    def save_state(self):
        state = {
            "stations": self.station_manager.get_stations_data(),
            "cars": self.get_cars_data(),  
            "deleted_stations": self.deleted_stations
        }
        DataPersistence.save_state(self.filepath, state)
