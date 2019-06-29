import sys
# sys.path.append('/development/timedata')

import bibliopixel

#causes frame timing information to be output
bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)

#Load driver for the AllPixel
from bibliopixel.drivers.timedata_visualizer import TimedataVisualizer

if __name__ == '__main__':
    #set number of pixels & LED type here
    driver = TimedataVisualizer(num=32)

    #load the LEDStrip class
    from bibliopixel.led import *
    led = LEDStrip(driver, threadedUpdate=True)

    #load channel test animation
    from bibliopixel.animation import StripChannelTest
    anim = StripChannelTest(led)

    try:
        anim.run(threaded=False)
    finally:
        anim.cleanup()
