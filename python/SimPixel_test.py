import sys
# sys.path.append('/development/timedata')

import bibliopixel

#causes frame timing information to be output
bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)

from BiblioPixelAnimations.matrix.bloom import Bloom

from bibliopixel.drivers.SimPixel import DriverSimPixel
from bibliopixel import LEDMatrix
from bibliopixel.animation import MatrixCalibrationTest
from bibliopixel.layout.circle import *
from bibliopixel.led import LEDCircle

x = y = 32

if not False:
    driver = DriverSimPixel(x * y, layout=None)
    led = LEDMatrix(driver, width=x, height=y)
    # anim = MatrixCalibrationTest(led)
    anim = Bloom(led)

else:
    pixels_per = [1, 4, 8, 12, 18, 24, 32, 40, 52, 64]
    rings, steps = gen_circle(rings=None, pixels_per=pixels_per, offset=0, invert=False)
    points = point_list_from_rings(rings, origin=(200, 200, 0), z_diff=8)
    driver = DriverSimPixel(sum(pixels_per), port=1337, layout=points)
    led = LEDCircle(driver, rings=rings, maxAngleDiff=0)

anim.run()


#from BiblioPixelAnimations.circle.diag import Diag
# from simplex import Simplex
import time
import sys

log.setLogLevel(log.DEBUG)

led = LEDMatrix(driver, coordMap=None,
                rotation=Rotation.ROTATE_0, vert_flip=False, serpentine=True,
                threadedUpdate=False, masterBrightness=255, pixelSize=(1, 1))

# x, y, z = (12, 12, 12)
# driver = DriverWebVis(x * y * z, point_list=None)
# led = LEDCube(driver, x, y, z, coordMap=gen_cube(x, y, z),
#               threadedUpdate=False, masterBrightness=255)
