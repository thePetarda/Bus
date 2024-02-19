import ast
import os
import pandas


#funkcja usuwa tekst z plików, do których nie udało się pobrać danych
def clean_files(catalog):
    i = 0
    path = catalog + "//bus" + str(i) + ".txt"
    while os.path.exists(path):
        if os.path.getsize(path) == 0:
            i += 1
            path = catalog + "//bus" + str(i) + ".txt"
            continue
        with open(path, 'r+') as file:
            first = file.read()[0]
            if first != "[":
                file.truncate(0)
        i += 1
        path = catalog + "//bus" + str(i) + ".txt"


# funkcja zamienia pobrane dane o pozycjach autobusów na Dataframe i zapisuje je
def to_data_frame(catalog):
    dfs = []
    i = 0
    path = catalog + "//bus" + str(i) + ".txt"
    while os.path.exists(path):
        if os.path.getsize(path) == 0:
            i += 1
            path = catalog + "//bus" + str(i) + ".txt"
            continue
        with open(path, "r") as file:
            data = ast.literal_eval(file.read())
            for el in data:
                df = pandas.DataFrame(el, index=[0])
                dfs.append(df)
        i += 1
        path = catalog + "//bus" + str(i) + ".txt"
    result_df = pandas.concat(dfs, ignore_index=True)
    result_df.to_json(f"processed/{catalog}.json")
    return result_df


# funkcja pobiera dane o pozycjach autobusów w postaci Dataframe
def read_data(catalog):
    return pandas.read_json(f"processed/{catalog}.json")


def main():
    # catalog = "bus2024_02_06_ 12_45_18"
    # catalog = "bus2024_02_04_ 15_31_43"
    catalog = "bus2024_02_03_ 22_30_02"
    clean_files(catalog)
    print(to_data_frame(catalog))
    print(read_data(catalog))


if __name__ == "__main__":
    main()
