class Car:
    def __init__(self, car_type, license_plate, is_express=False, skip_stations=None):
        
        car_type = car_type.lower()
        if car_type not in ["estandar", "suv"]:
            raise ValueError("Tipo de auto inválido. Debe ser 'estandar' o 'suv'.")
        
        self.car_type = car_type
        self.license_plate = license_plate
        self.extra_time = 5 if car_type == "suv" else 0
        self.is_express = is_express
        self.skip_stations = skip_stations if skip_stations else []
        self.processed_station = None 
        self.current_station = None  
        self.previous_stations = []  

    def get_processing_time(self, base_time):
        return base_time + self.extra_time
    
    
    
    
    def __str__(self):
        tipo = "Exprés" if self.is_express else self.car_type.capitalize()
        return f"{tipo} ({self.license_plate})"
