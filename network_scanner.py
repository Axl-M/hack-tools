#!/usr/bin/env python3

# This util is similar netdiscover util.
# Send ARP request to all (broadcast), receive answers and parse them.
# As result you can see IP-addresses who are in our network and their MAC-addresses.
# You must have scapy installed. Scapy not installed in python3. (Use command:  pip3 install scapy-python3).
# Be sure that you have scapy installed in the same version of python you are going
# to use for this util (python2 or python3).


import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    args = parser.parse_args()
    return args

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
        # print(element[1].psrc + "\t" + element[1].hwsrc)
    return client_list


def print_result(results_list):
    print("   IP\t\t\a   MAC address \n----------------------------------------------")
    for client in results_list:
        print(client['ip'] + '\t' + client['mac'])


options = get_arguments()
# scan_result = scan("10.0.2.0/24")
scan_result = scan(options.target)
print_result(scan_result)


