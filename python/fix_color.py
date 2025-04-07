#!/bin/env python3

import sys
from pathlib import Path
import re

COLOR_RE = re.compile("\x1b\d+m")

p = Path(sys.argv[1])
text = p.read_text()
p.write_text(COLOR_RE.rep("", text)
