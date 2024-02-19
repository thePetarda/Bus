import requests
import json
from collect_busses import create_dir


# funkcja zbiera dane o położeniu przystanków
def get_stops(api_key):
    url = "https://api.um.warszawa.pl/api/action/dbstore_get?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey="
    url += api_key
    response = requests.get(url)
    data = response.text
    return data


# funkcja zapisuje dane o położeniu przystanków
def load_stops(api_key, directory):
    create_dir(directory)
    routes = get_stops(api_key)
    path = directory + "\\stops.json"
    with open(path, "w") as file:
        file.write(str(routes))


def main():
    api_key = "efdf77db-cfc6-4cc8-8f53-34bda9d70dea"
    catalog = "timetables"
    load_stops(api_key, catalog)


if __name__ == "__main__":
    main()
