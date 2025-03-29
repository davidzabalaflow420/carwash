import json
import os

class DataPersistence:

    @staticmethod
    def save_state(filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_state(filename):
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return json.load(file)
        return None  