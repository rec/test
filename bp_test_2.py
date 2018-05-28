import bibliopixel

# causes frame timing information to be output
bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)

# Load driver for the AllPixel
from bibliopixel.drivers.serial import *
# set number of pixels & LED type here
driver = Serial(num = 160, ledtype = LEDTYPE.LPD8806)

# load the LEDStrip class
from bibliopixel.layout import *
led = Strip(driver)

# load channel test animation
from BiblioPixelAnimations.strip import PartyMode
anim = PartyMode.PartyMode(led)
print(PartyMode.__file__)

try:
    # run the animation
    anim.run(fps=10)
except KeyboardInterrupt:
    # Ctrl+C will exit the animation and turn the LEDs offs
    led.all_off()
    led.update()
