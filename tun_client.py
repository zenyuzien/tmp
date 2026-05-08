
#!/usr/bin/python3
import fcntl, struct, os, socket
from scapy.all import *

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_NO_PI = 0x1000

SERVER_IP   = "10.0.2.5"
SERVER_PORT = 9090

tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'tun%d', IFF_TUN | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    packet = os.read(tun, 2048)
    pkt = IP(packet)
    print("Sending: {} --> {}".format(pkt.src, pkt.dst))
    sock.sendto(packet, (SERVER_IP, SERVER_PORT))
