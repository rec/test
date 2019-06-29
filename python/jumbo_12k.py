import os, sys

PARENT = os.path.dirname(os.getcwd())
sys.path.append(os.path.join(PARENT, 'BiblioPixelAnimations'))

from BiblioPixelAnimations.matrix.bloom import Bloom
from bibliopixel.drivers.serial_driver import DriverTeensySmartMatrix
from bibliopixel import LEDMatrix
import bibliopixel.colors as colors
from bibliopixel import MultiMapBuilder, mapGen
import bibliopixel.log as log
import time
from bibliopixel import font

log.setLogLevel(log.DEBUG)

w = 128
h = 32
dCount = 3
d_order = [10, 11, 12]

build = MultiMapBuilder()
drivers = []
for i in range(dCount):
    build.addRow(mapGen(w, h, serpentine=False))
    drivers.append(DriverTeensySmartMatrix(width=w, height=h, deviceID=d_order[i]))

# print(build.map)

led = LEDMatrix(drivers, width=w, height=h * dCount, coordMap=build.map,
                threadedUpdate=not True, masterBrightness=128)

anim = Bloom(led)
try:
    anim.run(amt=6, fps=6)
finally:
    anim.cleanup()
    time.sleep(1)
    led.all_off()
    led.update()
    time.sleep(1)
    led.all_off()
    led.update()
TinyTest
