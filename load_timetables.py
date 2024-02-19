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
                # route["typ"] = stop["typ"]
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
            # TODO use regex
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


# def get_routes(line):
#     directory = "timetables"
#     routes = np.empty(4)
#     with open(directory + "/route.json") as f:
#         data = json.loads(f.read())
#     data = data["result"]
#     if line not in data.keys():
#         return pd.DataFrame()
#     data = data[line]
#     for trace in data.keys():
#         list = data[trace]
#         for el in list.keys():
#             stop = list[el]
#             routes = np.vstack([routes, [stop["nr_zespolu"], stop["typ"], stop["nr_przystanku"], trace]])
#     return pd.DataFrame(routes, columns=["zespol", "typ", "slupek", "trasa"])


# def get_stops():
#     directory = "timetables"
#     stops = []
#     with open(directory + "/stops.json") as f:
#         data = json.loads(f.read())
#     data = data["result"]
#     for stop in data:
#         stop = stop["values"]
#         place = {}
#         for el in stop:
#             if el["key"] == "zespol":
#                 place[el["key"]] = el["value"]
#             if el["key"] == "slupek":
#                 place[el["key"]] = el["value"]
#             if el["key"] == "szer_geo":
#                 place[el["key"]] = el["value"]
#             if el["key"] == "dlug_geo":
#                 place[el["key"]] = el["value"]
#         stops.append(place)
#     return pd.DataFrame(stops)


# def get_timetables(line):
#     time_files = []
#     timetables = []
#     directory = "timetables"
#     name = 'timetable_' + str(line) + '_'
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             # TODO use regex
#             if name in file:
#                 time_files.append(file)
#     for file in time_files:
#         words = file.split("_")
#         zespol = words[2]
#         slupek = words[3][0: 2]
#         with open(directory + "\\" + file, "r") as f:
#             data = ast.literal_eval(f.read())
#             data = data["result"]
#             for list in data:
#                 list = list["values"]
#                 time = {}
#                 time["zespol"] = zespol
#                 time["slupek"] = slupek
#                 for el in list:
#                     if el["key"] == "brygada":
#                         time[el["key"]] = el["value"]
#                     if el["key"] == "trasa":
#                         time[el["key"]] = el["value"]
#                     if el["key"] == "czas":
#                         time[el["key"]] = el["value"]
#                 timetables.append(time)
#     return pd.DataFrame(timetables)


# def get_timetables():
#     path = "timetables/timetables.json"
#     time_df = pd.read_json(path)
#     return time_df


# def get_timetables(line, stop_id, stop_nr):
#     timetables = []
#     path = 'timetables/timetable_' + str(line) + '_' + str(stop_id) + '_' + str(stop_nr) + '.txt'
#     if not os.path.exists(path):
#         return pd.DataFrame()
#     with open(path, "r") as f:
#         data = ast.literal_eval(f.read())
#         data = data["result"]
#         for list in data:
#             list = list["values"]
#             time = {}
#             time["zespol"] = stop_id
#             time["slupek"] = stop_nr
#             for el in list:
#                 if el["key"] == "brygada":
#                     time[el["key"]] = el["value"]
#                 if el["key"] == "trasa":
#                     time[el["key"]] = el["value"]
#                 if el["key"] == "czas":
#                     time[el["key"]] = el["value"]
#             timetables.append(time)
#     return pd.DataFrame(timetables)


# def join_routes(line, stops):
#     routes = get_routes(line)
#     if routes.empty:
#         return pd.DataFrame()
#     routes = pd.merge(routes, stops, on=["zespol", "slupek"], how="inner")
#     routes["dlug_geo"] = routes["dlug_geo"].apply(float)
#     routes["szer_geo"] = routes["szer_geo"].apply(float)
#     return routes


# def get_all_routes(df: pd.DataFrame):
#     stops = get_stops()
#     routes_df = []
#     for line in df["Lines"].unique():
#         route = join_routes(line, stops)
#         route["Lines"] = line
#         routes_df.append(route)
#     routes_df = pd.concat(routes_df, ignore_index=True)
#     return routes_df

# def join_timetables(line, stops):
#     timetables = get_timetables(line)
#     routes = get_routes(line)
#     if timetables.empty or routes.empty:
#         return pd.DataFrame()
#     routes = pd.merge(routes, stops, on=["zespol", "slupek"], how="inner")
#     # timetables = pd.merge(timetables, stops, on=["zespol", "slupek", "trasa"])
#     timetables = pd.merge(timetables, stops, on=["zespol", "slupek"])
#     return timetables


# def get_all_timetables(df: pd.DataFrame):
#     stops = get_stops()
#     timetables_df = []
#     for line in df["Lines"].unique():
#         timetable = join_timetables(line, stops)
#         timetable["Lines"] = line
#         timetables_df.append(timetable)
#     timetables_df = pd.concat(timetables_df, ignore_index=True)
#     return timetables_df
