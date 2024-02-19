import requests
import time
import json
import os
from datetime import datetime


# funkcja pobiera dane o pozycjach autobusów ze strony
def get_bus_positions(api_key):
    url = "https://api.um.warszawa.pl/api/action/busestrams_get"
    params = {
        'resource_id': 'f2e5503e-927d-4ad3-9500-4ab9e55deb59',
        'apikey': api_key,
        'type': '1'
    }

    response = requests.get(url, params=params)
    data = response.text
    data = json.loads(data)
    data = data["result"]
    return data


def create_dir(catalog):
    if not os.path.exists(catalog):
        os.makedirs(catalog)


# funkcja koordynuje pobieranie pozycji autobusów przez godzinę co minutę
def load_data(api_key, catalog):
    duration_in_seconds = 3600
    interval_in_seconds = 60

    start_time = time.time()
    current_time = start_time
    i = 0

    datetime_obj = datetime.fromtimestamp(start_time)
    time_string = datetime_obj.strftime("%Y_%m_%d_ %H_%M_%S")
    catalog = catalog + time_string
    create_dir(catalog)

    while current_time - start_time < duration_in_seconds:
        bus_positions = get_bus_positions(api_key)

        with open(catalog + "\\bus" + str(i) + ".txt", "a") as file:
            file.write(str(bus_positions))

        time.sleep(interval_in_seconds)
        current_time = time.time()
        i += 1


def main():
    api_key = "efdf77db-cfc6-4cc8-8f53-34bda9d70dea"
    catalog = "bus"
    load_data(api_key, catalog)


if __name__ == "__main__":
    main()
