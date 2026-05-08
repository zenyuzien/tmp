#!/usr/bin/env python3

import fcntl
import struct
import os
from socket import *

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_NO_PI = 0x1000

# Create TUN interface
tun = os.open("/dev/net/tun", os.O_RDWR)

ifr = struct.pack('16sH', b'tun%d', IFF_TUN | IFF_NO_PI)

ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)

ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")

print("Server Interface:", ifname)

# UDP socket
sock = socket(AF_INET, SOCK_DGRAM)

sock.bind(("0.0.0.0", 9090))

while True:

    data, addr = sock.recvfrom(2048)

    print("Received from:", addr)

    os.write(tun, data)
