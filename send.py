#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct

from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

def main():

    if len(sys.argv)<4:
        print 'pass 3 arguments: <destination> <src_port> <dst_port>'
        exit(1)

    if int(sys.argv[2]) <= 1024:
        print 'src_port must be greater than 1024'
        exit(1)

    if int(sys.argv[3]) <= 3000 or int(sys.argv[3]) >= 5000:
        print 'dst_port must be greater than 3000 and less than 5000'
        exit(1)

    my_host = socket.gethostname()
    my_ip = socket.gethostbyname(my_host)

    addr = socket.gethostbyname(sys.argv[1])
    iface = get_if()

    print "sending on interface %s to %s" % (iface, str(addr))
    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt /IP(dst=addr,src='10.0.1.1') / TCP(dport=int(sys.argv[3]), sport=int(sys.argv[2])) / "Hello, world!"
    pkt.show2()
    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()