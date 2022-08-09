import requests
import json
import gzip
import bs4
import threading
from queue import Queue
import pickle

BASE_URL = "https://samples.adsbexchange.com/readsb-hist"
data_folder_path = './data/'


def write_to_pickle(_url: str, _filename: str) -> None:
    _fout = open(f"{data_folder_path}{_filename}.pickle", "wb")
    pickle.dump(get_data_from_gz_url(_url), _fout)


def get_all_gzs_from_day(_year: int, _month: int, _day: int) -> list[str]:
    _url = f"{BASE_URL}/{_year:>04}/{_month:>02}/{_day:>02}/"
    data = requests.get(_url)
    unique_urls = set()
    soup = bs4.BeautifulSoup(data.content, 'html5lib')
    for link in soup.find_all("a"):
        unique_urls.add(str(link)[len('<a href=""') - 1:(-1 * len('">235955Z.json.gz</a>'))])
    return list(unique_urls)


def get_data_from_gz_url(_url: str = "") -> dict:
    """
    Get dictionary data from one gz url
    :param _url: the url to get data from
    :return: the dictionary to get data from
    """
    # print(f"\t--{_url} --", end="")
    if _url == "":
        raise ValueError("url must be supplied")
    data = requests.get(_url)
    jsongz = data.content
    json_str = gzip.decompress(jsongz).decode()
    actual_data = json.loads(json_str)
    # print("done")
    return actual_data


def perform_download(q):
    while not q.empty():
        _iterator, _url, _filename = q.get()
        # print(_iterator)
        write_to_pickle(_url, _filename)
        q.task_done()


def main():
    year = 2022
    month = 5
    day = 1
    url = f"{BASE_URL}/{year:>04}/{month:>02}/{day:>02}/"
    print(f"Gathering links from {year:>04}{month:>02}{day:>02}")
    gz_file_names = get_all_gzs_from_day(2022, 5, 1)
    print(f"working with {len(gz_file_names)} files")
    jobs = Queue()
    for i, jsongz_url in enumerate(gz_file_names):
        if jsongz_url.endswith(".gz"):
            short_name = jsongz_url[:len("json.gz")]
            jobs.put((i, f"{url}{jsongz_url}", short_name))
    print("loaded all jobs")
    for i in range(10):
        worker = threading.Thread(target=perform_download, args=(jobs,))
        worker.start()
    jobs.join()
    print("Downloading Finished")


if __name__ == "__main__":
    main()
