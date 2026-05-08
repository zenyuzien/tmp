#!/usr/bin/env python3

import fcntl
import struct
import os
import socket

from scapy.all import *

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_NO_PI = 0x1000

SERVER_IP   = "10.0.2.5"
SERVER_PORT = 9090

# Create TUN interface
tun = os.open("/dev/net/tun", os.O_RDWR)

ifr = struct.pack('16sH', b'tun%d', IFF_TUN | IFF_NO_PI)

ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)

ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")

print("Client Interface:", ifname)

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:

    packet = os.read(tun, 2048)

    ip = IP(packet)

    print("Sending packet:", ip.src, "->", ip.dst)

    sock.sendto(packet, (SERVER_IP, SERVER_PORT))
