#!/usr/bin/env python3

from math import tau, sin, cos
from struct import pack

N_POINTS = int(1e3)

qi = [[cos(tau*i/100), sin(tau*i/100)] for i in range(int(N_POINTS))]
flat = [item for sublist in qi for item in sublist]
buf = pack('%sf' % len(flat), *flat)


with open('/dev/stdout', 'wb') as out:
    out.write(buf)
