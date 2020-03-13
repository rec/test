import schedule
import time


def two_seconds():
    print('tick')
    time.sleep(2)
    print('tock')


schedule.every().second.do(two_seconds)
while True:
    schedule.run_pending()
    time.sleep(1)
