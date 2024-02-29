import socket
import sys

from datetime import datetime


class PortScanner:

    def __init__(self, targets: list, ports: list):
        self.targets = targets
        self.ports   = ports


def main():
    
    targets_input = sys.argv[1]     # endreço único, ou rede xxx.xxx.xxx/xx
    ports_input   = sys.argv[2]     # range de portas na forma xxxxx-yyyyy

    targets = list()
    ports   = list()

    if "/" in targets_input:
        address, netmask = targets_input.split("/")
        octets = address.split(".")
        processed_octets = list()
        address = "0b"
        
        for octet in octets:
            octet = bin(int(octet))[2:]
            while len(octet) < 8: octet = "0" + octet
            address += octet
                
        address = int(address[2:], base=2)
        netmask = int(netmask)
        netmask = "1" * netmask + "0" * (32 - netmask)
        netmask = bin(int(netmask, base=2))
        netmask = int(netmask[2:], base=2)
        print(address & netmask)


if __name__ == "__main__":
    main()