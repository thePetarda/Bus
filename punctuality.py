from load_timetables import read_timetables
import pandas as pd
from speed import to_meters
from datetime import timedelta
import folium
import webbrowser


# funkcja łączy odpowiednie pozycje autobusów z odpowiednimi rozkładami jazdy i przystankami
def join_df(bus_df: pd.DataFrame, time_df: pd.DataFrame, speed):
    speed_df = pd.DataFrame(speed.tolist(), columns=['Velosity', 'Lat', 'Lon', 'Lines', 'Time'])
    bus_df = pd.merge(bus_df, speed_df, on=['Lat', 'Lon', 'Lines', 'Time'])
    bus_df['Time'] = pd.to_datetime(bus_df['Time'], format='%Y-%m-%d %H:%M:%S')
    time_df['Time'] = pd.to_timedelta(time_df['Time'], errors='coerce')
    min_time = bus_df["Time"].min()
    min_time = timedelta(hours=min_time.hour, minutes=min_time.minute, seconds=min_time.second)
    max_time = bus_df["Time"].max()
    max_time = timedelta(hours=max_time.hour, minutes=max_time.minute, seconds=max_time.second)
    time_df["Brigade"] = time_df["Brigade"].astype(str)
    # time_df = time_df[time_df['Time'] >= min_time]
    # time_df = time_df[time_df['Time'] <= max_time]
    df = pd.merge(time_df, bus_df, on=["Brigade", "Lines"], suffixes=["_stop", "_bus"])
    return df


# funkcja ocenia czy autobus przyjeżdża punktualnie na dany przystanek
def calc_punctuality(row):
    time = row["Time_diff"]
    dist = to_meters(row['Lat_stop'], row['Lon_stop'], row['Lat_bus'], row['Lon_bus']) / 1000
    if time == 0:
        if dist < 5:
            return True
        return False
    t = timedelta(minutes=5).total_seconds() / 3600
    velosity = row["Velosity"]
    t += dist / velosity
    if time <= t:
        return True
    return False


def time_diff(row):
    time_s = row["Time_stop"]
    time_b = row["Time_bus"]
    time_b = timedelta(hours=time_b.hour, minutes=time_b.minute, seconds=time_b.second)
    time = abs(time_s - time_b)
    time = time.total_seconds() / 3600
    return time


# funkcja przedtawia spóźnione autobusy na mapie Warszawy
def create_map(data: pd.DataFrame):
    map = folium.Map(location=[52.239, 21.045], zoom_start=10)
    for index, el in data.iterrows():
        if not el["Puntual"]:
            dist = to_meters(el['Lat_stop'], el['Lon_stop'], el['Lat_bus'], el['Lon_bus']) / 1000
            velosity = el["Velosity"]
            late = dist / velosity * 60
            late = str(round(late, 1)) + 'min'
            popup = f"Line : {el['Lines']} \n Stop : {el['Stop_team']}({el['Stop_nr']})"
            folium.Marker(location=[el['Lat_stop'], el['Lon_stop']], popup=popup, tooltip=late).add_to(map)
    map.save("map_punc.html")
    webbrowser.open("map_punc.html")


# funkcja bada punktualność autobusów
def proc_puntuality(bus_df: pd.DataFrame, speed):
    time_df = read_timetables()
    df = join_df(bus_df, time_df, speed)
    df["Time_diff"] = df.apply(time_diff, axis=1)
    df = df[df['Time_diff'] <= 0.5]
    min_ind = df.groupby(['Stop_team', 'Stop_nr', 'Time_stop', 'Lines', 'Brigade'])['Time_diff'].idxmin()
    df = df.loc[min_ind]
    df["Puntual"] = df.apply(calc_punctuality, axis=1)
    punc_num = df['Puntual'].sum()
    proc = round(punc_num / len(df) * 100, 2)
    print(f"number of buses that were puntual: {punc_num} ({proc} %)")
    create_map(df)
