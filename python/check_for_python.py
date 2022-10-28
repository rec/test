import time
import requests

SLEEP = 1
URL = 'https://docs.python.org/3/whatsnew/3.11.html'


def run():
    count = 0
    status_code = 0
    while not (200 <= status_code < 300):
        time.sleep(SLEEP)
        print('.', end='')
        count += 1
        if not count % 32:
            print()

        status_code = requests.get(URL).status_code

    print('found', status_code)


run()
