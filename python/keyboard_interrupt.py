import time

print('one')
try:
    print('two')
    time.sleep(10)
except Exception as e:
    print('three', e)
finally:
    print('four')
