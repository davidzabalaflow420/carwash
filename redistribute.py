from stack import Stack

class Redistribute:
    def __init__(self, station_manager):
        self.station_manager = station_manager

    def redistribute_cars(self, removed_station):
       
        waiting_queue = removed_station.queue  

        while not waiting_queue.is_empty():
            car = waiting_queue.dequeue()  
            self.assign_car_to_available_station(car) 
    
    def assign_car_to_available_station(self, car):
       
        self.reorder_stations_for_express_car()

        for station in self.station_manager.get_stations().items:
            if station.queue.size() < 5:  
                station.add_car(car)  
                print(f"Auto {car} redistribuido a la estación {station.name}.")
                return  
        print(f"No se pudo redistribuir el auto {car}. Todas las estaciones están llenas.")

    def reorder_stations_for_express_car(self):
        temp_stack = Stack()
        express_station_order = []
        
        while not self.station_manager.stations.is_empty():
            station = self.station_manager.stations.pop()
            if station.is_optional:
                express_station_order.append(station)
            else:
                temp_stack.push(station)

        for station in express_station_order:
            temp_stack.push(station)

        while not temp_stack.is_empty():
            self.station_manager.stations.push(temp_stack.pop())
