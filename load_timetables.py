import os
import ast
import pandas as pd
import json


def get_routes():
    directory = "timetables"
    routes = []
    with open(directory + "/route.json") as f:
        data = json.loads(f.read())
    data = data["result"]
    for line in data.keys():
        route = {}
        route["linia"] = line
        line_data = data[line]
        for trace in line_data.keys():
            trace_data = line_data[trace]
            route["trasa"] = trace
            for el in trace_data.keys():
                stop = trace_data[el]
                route["zespol"] = stop["nr_zespolu"]
                route["slupek"] = stop["nr_przystanku"]
                routes.append(route)
    return pd.DataFrame(routes)


def get_stops():
    directory = "timetables"
    stops = []
    with open(directory + "/stops.json") as f:
        data = json.loads(f.read())
    data = data["result"]
    for stop in data:
        stop = stop["values"]
        place = {}
        for el in stop:
            if el["key"] == "zespol":
                place[el["key"]] = el["value"]
            if el["key"] == "slupek":
                place[el["key"]] = el["value"]
            if el["key"] == "kierunek":
                place[el["key"]] = el["value"]
            if el["key"] == "szer_geo":
                place[el["key"]] = float(el["value"])
            if el["key"] == "dlug_geo":
                place[el["key"]] = float(el["value"])
        stops.append(place)
    return pd.DataFrame(stops)


def get_timetables():
    time_files = []
    timetables = []
    directory = "timetables"
    name = 'timetable_'
    for root, dirs, files in os.walk(directory):
        for file in files:
            if name in file:
                time_files.append(file)
    for file in time_files:
        words = file.split("_")
        linia = words[1]
        zespol = words[2]
        slupek = words[3][0: 2]
        with open(directory + "\\" + file, "r") as f:
            data = ast.literal_eval(f.read())
            data = data["result"]
            for list in data:
                list = list["values"]
                time = {}
                time["linia"] = linia
                time["zespol"] = zespol
                time["slupek"] = slupek
                for el in list:
                    if el["key"] == "brygada":
                        time[el["key"]] = el["value"]
                    if el["key"] == "kierunek":
                        time[el["key"]] = el["value"]
                    if el["key"] == "trasa":
                        time[el["key"]] = el["value"]
                    if el["key"] == "czas":
                        time[el["key"]] = el["value"]
                timetables.append(time)
    return pd.DataFrame(timetables)


def join_timetables():
    timetables = get_timetables()
    routes = get_routes()
    stops = get_stops()
    routes = pd.merge(routes, stops, on=["zespol", "slupek"], how="inner")
    timetables = pd.merge(timetables, stops, on=["zespol", "slupek", "kierunek"])
    timetables = timetables.rename(columns={"linia": "Lines", "zespol": "Stop_team", "slupek": "Stop_nr", "brygada": "Brigade", "kierunek": "Direction", "trasa": "Route", "czas": "Time", "szer_geo": "Lat", "dlug_geo": "Lon"})
    timetables["Brigade"] = timetables["Brigade"].astype(str)
    timetables.to_json("processed/timetables.json")
    return timetables


def read_timetables():
    return pd.read_json("processed/timetables.json")


def main():
    time_df = join_timetables()
    print(time_df)
    print(read_timetables())


if __name__ == "__main__":
    main()
