# Bus

Bus is a project for analizing data of Warsaw buses. It creates a histogram of the speed of the busses and trams, calculates how many exceeded the speed of 50km/h and how many were late for their stops. The data is visualized on a map of Warsaw.

## Installation

clone the github repository

```bash
git clone https://github.com/thePetarda/Bus.git
```

## Usage

Change the apikey from https://api.um.warszawa.pl/# to your apikey in files: collect_busses.py, collect_stops.py, collect_timetables.py.
If you want to collect new bus data run the main function in collect_busses.py
If you want to analize given data choose the right file name in catalog in main.py and run the main.py