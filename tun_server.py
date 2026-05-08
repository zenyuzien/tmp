#!/usr/bin/python3
import fcntl, struct, os, socket
from scapy.all import *

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_NO_PI = 0x1000

PORT = 9090

# Create TUN
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'tun%d', IFF_TUN | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

os.system("ip addr add 192.168.53.98/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))
os.system("sysctl -w net.ipv4.ip_forward=1")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

while True:
    data, (ip, port) = sock.recvfrom(2048)
    pkt = IP(data)
    print("From tunnel: {} --> {}".format(pkt.src, pkt.dst))
    os.write(tun, data)
