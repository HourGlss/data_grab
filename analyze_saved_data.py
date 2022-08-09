import plotly.graph_objects as go
import pickle
from os import listdir
from os.path import isfile, join
from math import sin, cos, sqrt, atan2, radians
from flight import Flight
import download_data

ORIGIN = (10, 20)


def in_search_area(check_lat, check_lon, _distance_in_kms):
    R = 6373.0

    lat1 = radians(ORIGIN[0])
    lon1 = radians(ORIGIN[1])
    lat2 = radians(check_lat)
    lon2 = radians(check_lon)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance_km = R * c
    if distance_km < _distance_in_kms:
        return True
    return False


if __name__ == "__main__":
    # READ THIS
    # SERIOUSLY
    # BIG WASTE OF TIME IF YOU DO NOT!
    download_data.main()  # IF YOU HAVE DOWNLOADED ALREADY, COMMENT OUT
    #
    #
    #
    #
    #
    #

    flights = {}
    mypath = './data/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyfiles.sort()
    print(f"Dealing with {len(onlyfiles)} files!")
    for i, file in enumerate(onlyfiles):
        if file.endswith("pickle"):
            print(i)
            data = pickle.load(open(f'{mypath}{file}', 'rb'))
            for k, v in data.items():
                if k == "aircraft":
                    for e in v:
                        if 'hex' in e.keys() and 'lat' in e.keys() and 'lon' in e.keys():
                            if in_search_area(e['lat'], e['lon'], 50):
                                if e['hex'] not in flights.keys():
                                    flights[e['hex']] = Flight(e['hex'])
                                flights[e['hex']].add_coords(e['lat'], e['lon'])

    # IF YOU GRAPH MORE THAN YOU NEED, IT WILL CRASH.
    fig = go.Figure()
    for k, v in flights.items():
        temp = v.get_flight_path()
        # print(str(v)) # THIS WILL GIVE A SIMPLE VERSION
        fig.add_trace(temp)
    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 10, 'lat': 10},
            'style': "stamen-terrain",
            'zoom': 1})
    fig.show()
