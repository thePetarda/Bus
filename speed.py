import math
import pandas as pd
import matplotlib.pyplot as plt
import folium
from datetime import datetime
from load_data import to_data_frame, clean_files
import webbrowser


# funkcja zamienia położenie dwóch punktów na odległość między nimi w metrach
def to_meters(lat1, lon1, lat2, lon2):
    R = 6371000

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# funkcja łączy położenia autobusów z ich położeniami w kolejnym pomiarze
def join_df(df: pd.DataFrame):
    df = df.sort_values(by=['Lines', 'Brigade', 'Time'])
    df2 = df.shift(-1)
    df = df.add_suffix('_1')
    df2 = df2.add_suffix('_2')
    merged_df = pd.concat([df, df2], axis=1)
    merged_df = merged_df[merged_df['VehicleNumber_1'] == merged_df['VehicleNumber_2']]
    return merged_df


# funkcja oblicza prędkość autobusu
def calc_speed(row):
    time2 = datetime.strptime(row['Time_2'], "%Y-%m-%d %H:%M:%S")
    time1 = datetime.strptime(row['Time_1'], "%Y-%m-%d %H:%M:%S")
    if time1 == time2:
        return [0, row['Lat_1'], row['Lon_1'], row["Lines_1"], row["Time_1"]]
    time = abs(time2 - time1)
    dist = to_meters(row['Lat_1'], row['Lon_1'], row['Lat_2'], row['Lon_2'])
    velosity = dist/time.total_seconds()*3600/1000
    return [velosity, row['Lat_1'], row['Lon_1'], row["Lines_1"], row["Time_1"]]


def get_speed(df):
    df = join_df(df)
    ans = df.apply(calc_speed, axis=1)
    ans = ans[ans.apply(lambda x: x[0] != 0)]
    return ans


# funkcja przednawia histogram zmierzonych prędkości
def create_histogram(data: list):
    plt.hist([el[0] for el in data])
    plt.xlabel("prędkość autobusu [km/h]")
    plt.ylabel("ilość autobusów")
    plt.show()
    plt.savefig("Histogram_prędkość")


# funkcja oblicza ilość autobusów przekraczających prędkość
def count_over_50(data: list):
    ans = 0
    for el in data:
        if el[0] > 50:
            ans += 1
    return ans


# funkcja przedtawia autobusy przekraczające prędkość na mapie Warszawy
def create_map(data: list):
    map = folium.Map(location=[52.239, 21.045], zoom_start=10)
    for el in data:
        if el[0] > 50:
            popup = f"Line : {el[3]} \n Time {el[4]}"
            folium.Marker(location=[el[1], el[2]], popup=popup, tooltip=(str(round(el[0], 1)) + 'km/h')).add_to(map)
    map.save("map_speed.html")
    webbrowser.open("map_speed.html")


def proc_speed(df):
    data = get_speed(df)
    create_histogram(data)
    exceed_number = count_over_50(data)
    proc = round(exceed_number / len(data) * 100, 2)
    print(f"number of buses that exceeded the speed of 50 km/h: {exceed_number} ({proc} %)")
    create_map(data)
    return data
