# import soundfile as sf
# from numpy.testing import assert_array_equal

# import numpy as np
from pathlib import Path
from vl8.dsp import soundfile_io as sio
import tdir
import unittest

TEST_FILE = Path(__file__).parent / 'b-4098.wav'
DIR = Path(__file__).parent / 'sources'


@tdir
class TestSoundfile(unittest.TestCase):
    def test_soundfile_xxx(self):
        # A 24-bit file
        infile = DIR / 'sunnk - skinning gales 07.wav'
        outfile = Path('stereo.wav')
        d, sr = sio.read(infile)
        sio.write(outfile, d, sr)
