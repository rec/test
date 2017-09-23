from bibliopixel.animation import BaseAnimation
from bibliopixel import colors

# This is using the default 32x32 simpixel display -
# so this is a list of 16 * 64 = 1024 colors.
BASE = [
    colors.Black, colors.Black, colors.Black, colors.Black,
    colors.Green, colors.Green, colors.Green, colors.Green,
    colors.Blue, colors.Blue, colors.Blue, colors.Blue,
    colors.White, colors.White, colors.White, colors.White,
] * 64


class Scroll(BaseAnimation):
    def pre_run(self):
        self.layout.set_colors(BASE)

    def step(self, amt=1):
        # Pop a color off the end, and insert it at the start.
        self.layout._colors.insert(0, self.layout._colors.pop())
