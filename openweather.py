from INFO import API_KEYS
import requests
import pprint

openweather_api = API_KEYS.OPENWEATHERMAP_API

class City:
    def __init__(self, name, units="metric"):
        self.name = name
        self.units = units
        self.get_data()

    def get_data(self):
        try:
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={self.name}&units={self.units}&appid={openweather_api}")

        except:
            print("No internet access")

        response_json = response.json()
        self.temp = response_json["main"]["temp"]
        self.temp_min = response_json["main"]["temp_min"]
        self.temp_max = response_json["main"]["temp_max"]

    def temp_print(self):
        units_symbol = "C"
        if self.units == "imperial":
            units_symbol = "F"
        print(f"In {self.name} it is currently {self.temp} {units_symbol}")
        print(f"Today's High: {self.temp_max} {units_symbol}")
        print(f"Today's Low: {self.temp_min} {units_symbol}")

my_city = City("Tokyo")
my_city.temp_print()

vacation_city = City("new york", "imperial")
vacation_city.temp_print()

