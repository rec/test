ls | python3 <(cat <<EoF

import sys

for i, a in enumerate(sys.stdin):
    print i, a,
EoF
)
