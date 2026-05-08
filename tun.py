#!/usr/bin/env python3

import fcntl
import struct
import os
import time

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_NO_PI = 0x1000

# Open the clone device
tun = os.open("/dev/net/tun", os.O_RDWR)

# Create the tun interface
ifr = struct.pack('16sH', b'tun%d', IFF_TUN | IFF_NO_PI)

ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")

print("Interface Name:", ifname)

while True:
    time.sleep(10)
