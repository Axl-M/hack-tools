#!/usr/bin/env python3

# for Python version 3
# DESCRIPTION
# Util for changing MAC address for specified interface using Linux commands.
#
# use:
#   macchanger --help   for more info
# options:
#   -i, --interface     Interface to change its MAC address
#   -m, --mac           New MAC address
#   -m r                Generate random MAC address
# EXAMPLES:
# ./macchanger.py -i eth0 -m 00:01:02:03:04:77
# or
# ./macchanger.py -i eth0 -m r


import subprocess
import argparse
import re
import random


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
    args = parser.parse_args()
    if not args.interface:
        parser.error('[-] Please specify an interface, use --help for more info.')
    if not args.new_mac:
        parser.error('[-] Please specify a new MAC address, use --help for more info.')
    if args.new_mac == 'r':
        choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f']
        rand_for_mac = []
        for x in range(0, 13):
            rand_for_mac.append(random.choice(choices))
        args.new_mac = str(rand_for_mac[1] + rand_for_mac[2] + ':' + rand_for_mac[3] + rand_for_mac[4] + ':'\
                                 + rand_for_mac[5] + rand_for_mac[6] + ':' + rand_for_mac[7] + rand_for_mac[8] + ':'\
                                 + rand_for_mac[9] + rand_for_mac[10] + ':' + rand_for_mac[11] + rand_for_mac[12])
    return args


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    print('...')
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_call(['ifconfig', interface])
    print(ifconfig_result)
    mac_address_search_result = re.search(r'(\w\w:){5}\w\w', str(ifconfig_result))
    print(mac_address_search_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


args = get_arguments()
print(args)
print(args.interface)
print(args.new_mac)
current_mac = get_current_mac(args.interface)
# change_mac(args.interface, args.new_mac)
# print("                   Previous MAC address was: " + str(current_mac))
# current_mac = get_current_mac(args.interface)
# if current_mac == args.new_mac:
#     print("[+] MAC address was successfully changed to: " + current_mac)
# else:
#     print("[-]  <<   MAC address DID NOT get changed !!!   >>")
