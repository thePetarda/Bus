import requests
import json
import os
from collect_busses import create_dir


# funkcja pobiera dane o trasach autobusów
def get_routes(api_key):
    url = "https://api.um.warszawa.pl/api/action/public_transport_routes/?apikey="
    url += api_key
    response = requests.get(url)
    data = response.text
    data = json.loads(data)
    data = data["result"]
    return data


# funkcja pobiera dane o rozkładzie jazdy dla konkretnej linii i konkretnego przystanku
def get_timetables(api_key, stop_id, stop_nr, line):
    url = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId=' + stop_id + '&busstopNr=' + stop_nr + '&line=' + line + '&apikey=' + api_key
    response = requests.get(url)
    data = response.text
    data = json.loads(data)
    return data


# funkcja koordynuje ładowanie rozkłądów jazdy
def load_timetables(api_key, directory):
    create_dir(directory)
    routes = get_routes(api_key)
    path = directory + "\\route.txt"
    if not os.path.exists(path):
        with open(path, "w") as file:
            file.write(str(routes))
    for line in routes.keys():
        lines = routes[line]
        for track in lines:
            tracks = lines[track]
            for number in tracks:
                stop_id = tracks[number]['nr_zespolu']
                stop_nr = tracks[number]['nr_przystanku']
                path = directory + f"\\timetable_{line}_{stop_id}_{stop_nr}.txt"
                if not os.path.exists(path):
                    timetable = get_timetables(api_key, stop_id, stop_nr, line)
                    with open(directory + f"\\timetable_{line}_{stop_id}_{stop_nr}.txt", "w") as file:
                        file.write(str(timetable))


def main():
    api_key = "efdf77db-cfc6-4cc8-8f53-34bda9d70dea"
    catalog = "timetables"
    load_timetables(api_key, catalog)


if __name__ == "__main__":
    main()

# https://api.um.warszawa.pl/api/action/public_transport_routes/?apikey=efdf77db-cfc6-4cc8-8f53-34bda9d70dea
# https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId=5073&busstopNr=06&line=184&apikey=efdf77db-cfc6-4cc8-8f53-34bda9d70dea
# https://api.um.warszawa.pl/api/action/dbstore_get?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey=efdf77db-cfc6-4cc8-8f53-34bda9d70dea
