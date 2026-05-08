#!/usr/bin/python3
import fcntl, struct, os
from scapy.all import *

TUNSETIFF = 0x400454ca
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

tap = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'tap%d', IFF_TAP | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tap, TUNSETIFF, ifr)
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

while True:
    packet = os.read(tap, 2048)
    ether = Ether(packet)
    print(ether.summary())
    if ARP in ether and ether[ARP].op == 1:
        arp = ether[ARP]
        newether = Ether(dst=ether.src, src="aa:bb:cc:dd:ee:ff")
        newarp = ARP(op=2, hwsrc="aa:bb:cc:dd:ee:ff", psrc=arp.pdst, hwdst=arp.hwsrc, pdst=arp.psrc)
        newpkt = newether/newarp
        print("Fake ARP reply: {}".format(newpkt.summary()))
        os.write(tap, bytes(newpkt))
