import requests
import json
import gzip
import bs4
import threading

import queue
from math import sin, cos, sqrt, atan2, radians

from flight import Flight

ORIGIN = (37.249996937265166, -115.81276270345806)


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


BASE_URL = "https://samples.adsbexchange.com/readsb-hist"


def get_all_gzs_from_day(_year: int, _month: int, _day: int) -> list[str]:
    _url = f"{BASE_URL}/{_year:>04}/{_month:>02}/{_day:>02}/"
    data = requests.get(_url)
    unique_urls = set()
    soup = bs4.BeautifulSoup(data.content, 'html5lib')
    for link in soup.find_all("a"):
        unique_urls.add(str(link)[len('<a href=""') - 1:(-1 * len('">235955Z.json.gz</a>'))])
    return list(unique_urls)


def get_data_from_gz_url(_url: str = "") -> dict:
    data = requests.get(_url)
    jsongz = data.content
    json_str = gzip.decompress(jsongz).decode()
    actual_data = json.loads(json_str)
    return actual_data


def perform_download(q: queue.Queue):
    while not q.empty():
        _url, _flights, _flights_lock = q.get()
        _data = get_data_from_gz_url(_url)
        for _k, _v in _data.items():
            if _k == "aircraft":
                for _e in _v:
                    if 'hex' in _e.keys() and 'lat' in _e.keys() and 'lon' in _e.keys():  # THIS COULD BE BETTER
                        # ONLY BUILD FLIGHTS WITHIN THE SEARCH RADIUS
                        if in_search_area(_e['lat'], _e['lon'], 50):  # CURRENTLY 50 km from ORIGIN
                            _flights_lock.acquire()  # Need to make this next part thread-safe
                            if _e['hex'] not in _flights.keys():
                                _flights[_e['hex']] = Flight(_e['hex'])
                            _flights[_e['hex']].add_coords(_e['lat'], _e['lon'])
                            _flights_lock.release()  # Release when done with flights dict
        q.task_done()


if __name__ == "__main__":
    year = 2022
    month = 5
    day = 1
    flights = {}
    flight_lock = threading.Lock()
    url = f"{BASE_URL}/{year:>04}/{month:>02}/{day:>02}/"
    print(f"Gathering links from {year:>04}{month:>02}{day:>02}")
    gz_file_names = get_all_gzs_from_day(2022, 5, 1)
    print(f"working with {len(gz_file_names)} files")
    jobs = queue.Queue()
    for i, jsongz_url in enumerate(gz_file_names):
        if jsongz_url.endswith(".gz"):
            jobs.put((f"{url}{jsongz_url}", flights, flight_lock))
    print("loaded all jobs")
    for i in range(10): # Run 10 downloads at a time. For optimal speed you can mess with this number
        worker = threading.Thread(target=perform_download, args=(jobs,))
        worker.start()
    jobs.join()
    print("Actually done -- STARTING WRITE")
    # Here we are dumping to a file
    fout = open("record.log", "w")
    for k, v in flights.items():
        fout.write(str(v))
    fout.close()
    print("Finished Writing")
