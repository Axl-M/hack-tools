# hack-tools
# ethical-hacking
Ethical Hacking Scripts in Python and Shell for OSX / Linux

MAC_CHANGER - 
version for python 2x and python 3x
**DESCRIPTION**

Util for changing MAC address for specified interface using Linux commands.


Usage:

```sh
    $ python3 macchanger.py -i <interface> -m <mac>
```  


macchanger --help   for more info

 options:
 
  -i, --interface     Interface to change its MAC address
  
  -m, --mac           New MAC address
  
  -m r                Generate random MAC address
  
EXAMPLES:

./macchanger.py -i eth0 -m 00:01:02:03:04:77

or

./macchanger.py -i eth0 -m r


NETWORK SCANNER
This util is similar netdiscover util.
Send ARP request to all (broadcast), receive answers and parse them.
As result you can see IP-addresses who are in our network and their MAC-addresses.
You must have scapy installed. Scapy not installed in python3. (Use command:  pip3 install scapy-python3).
Be sure that you have scapy installed in the same version of python you are going
to use for this util (python2 or python3).

./network_scanner.py -t 10.0.2.0/24

-t  -target
and specify IP-adress or range

#ARP_SPOOF - for MITM attack.

#PACKET_SNIFER - to capture URLs, passwords, logins from trafic.

