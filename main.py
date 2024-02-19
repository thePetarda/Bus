from load_data import read_data, clean_files
from speed import proc_speed
from punctuality import proc_puntuality


def main():
    catalog = "bus2024_02_03_ 22_30_02"
    # catalog = "test2"
    clean_files(catalog)
    df_bus = read_data(catalog)
    speed = proc_speed(df_bus)
    print(speed)
    proc_puntuality(df_bus, speed)


if __name__ == "__main__":
    main()
