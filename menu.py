import random
import string
import json
from car_wash import CarWashSystem
from data_persistence import DataPersistence

def generar_placa():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=3))
    return letras + numeros

def generar_auto(system):
    tipo_auto = input("Ingrese el tipo de auto (SUV/Estandar): ").strip().upper()
    while tipo_auto not in ["SUV", "ESTANDAR"]:
        print("Tipo de auto inválido. Debe ser 'SUV' o 'Estandar'.")
        tipo_auto = input("Ingrese el tipo de auto (SUV/Estandar): ").strip().upper()
    
    express = input("¿Es exprés? (si/no): ").strip().lower() == "si"
    skip_stations = ["Prelavado"] if express else []
    
    placa = generar_placa()
    print(f"Placa generada: {placa} - Tipo: {tipo_auto.capitalize()}")
    print(f"Exprés: Saltará estación {skip_stations}" if express else "No es exprés")
    
    system.add_car(placa, tipo_auto.capitalize(), express, skip_stations)

def manejar_promocion_encerrado(system):
    accion = input("¿Desea activar o desactivar la promoción de encerado? (activar/desactivar): ").strip().lower()
    estaciones = [station.name for station in system.station_manager.get_stations().values()]

    if accion == "activar":
        if "Encerado" not in estaciones:
            system.add_station("Encerado", 6, is_optional=True)
            print("¡Promoción de encerado activada! Estación de Encerado agregada.")
        else:
            print("La estación Encerado ya está activa.🟢")
    elif accion == "desactivar":
        if "Encerado" in estaciones:
            system.remove_station("Encerado")
            print("🚫 Estación 'Encerado' eliminada con éxito.")
            print("Promoción de encerado desactivada.🔴")
        else:
            print("La estación Encerado ya estaba desactivada.")
    else:
        print("Opción inválida.❌")

def menu():
    system = CarWashSystem()
    
    saved_state = DataPersistence.load_state("car_wash_state.json")
    if saved_state and isinstance(saved_state, dict) and "stations" in saved_state:
        system.station_manager.load_from_state(saved_state)
        print("📥 Estado restaurado desde el archivo.")
    else:
        print("⚠️ No se pudo restaurar el estado. Usando configuración predeterminada.")

    opciones = {
        "1": lambda: generar_auto(system),
        "2": lambda: system.process_cars(),
        "3": lambda: system.restore_deleted_stations(),
        "4": lambda: eliminar_estacion(system),
        "5": lambda: manejar_promocion_encerrado(system),
        "6": lambda: activar_secado(system),
        "7": lambda: print(system.get_status()),
        "8": lambda: exit_menu(system)
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion in opciones:
            opciones[opcion]()
        else:
            print("Opción inválida.")


def mostrar_menu():
    print("\nLavado de Autos de David:")
    print("1. Generar un auto")
    print("2. Lavar autos")
    print("3. Restaurar estaciones fuera de servicio")
    print("4. Deshabilitar estación")
    print("5. Promoción de encerado")
    print("6. Activar/Desactivar secado")
    print("7. Consultar estado del sistema")
    print("8. Salir")

def eliminar_estacion(system):
    station_name = input("Ingrese el nombre de la estación a eliminar: ")
    system.remove_station(station_name)

def activar_secado(system):
    enable = input("¿Activar secado? (si/no): ").strip().lower() == "si"
    system.toggle_drying(enable)

def exit_menu(system):
    print("💾 Guardando estado antes de salir...")
    try:
        state_data = {
            "stations": system.station_manager.get_stations_data(),
            "cars": system.get_cars_data() 
        }
        DataPersistence.save_state("car_wash_state.json", state_data)
        print("✅ Estado guardado correctamente. Saliendo del sistema...")
    except AttributeError as e:
        print(f"❌ Error al guardar el estado: {e}")
    exit()


if __name__ == "__main__":
    menu()
