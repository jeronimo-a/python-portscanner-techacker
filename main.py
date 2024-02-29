import socket
import sys

from datetime import datetime


class PortScanner:


    WELL_KNOWN_PORTS = {
        20: 'FTP (File Transfer Protocol)',
        21: 'FTP (File Transfer Protocol)',
        22: 'SSH (Secure Shell)',
        23: 'Telnet',
        25: 'SMTP (Simple Mail Transfer Protocol)',
        53: 'DNS (Domain Name System)',
        80: 'HTTP (Hypertext Transfer Protocol)',
        110: 'POP3 (Post Office Protocol version 3)',
        143: 'IMAP (Internet Message Access Protocol)',
        443: 'HTTPS (HTTP Secure)',
        3306: 'MySQL',
        3389: 'Remote Desktop Protocol (RDP)',
    }

    
    def __init__(self, targets: list, ports: list):
        self.targets = targets
        self.ports   = ports

    
    def scan_host(self, host, port):
            
        try:

            curr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = curr_socket.connect_ex((host, port))

            if not result:
                print(f"\tPort {port} OPEN\tService:", end='')
                print(PortScanner.WELL_KNOWN_PORTS.get(port, "Unknown"))
                curr_socket.close()

            else:
                print(f"\tPort {port} CLOSED")

        except Exception as error:
            print("An error occurred: ", error)

    
    def scan_targets(self):

        print("Beggining port scan\n")
        for target in self.targets:
            target = number_to_ip(target)
            print(target)
            for port in self.ports:
                self.scan_host(target, port)
            print()
        

def generate_targets_from_cidr(targets_input):

    targets = list()

    address, netmask = targets_input.split("/")
    address = ip_to_number(address)[0]
            
    netmask = int(netmask)
    netmask = "1" * netmask + "0" * (32 - netmask)
    netmask = bin(int(netmask, base=2))[2:]
    netmask = int(netmask, base=2)
    network = address & netmask
    address = network + 1

    while address & netmask == network:
        targets.append(address)
        address += 1

    targets.pop()   # exclui o broadcast

    return targets


def number_to_ip(number):

    number = bin(number)[2:]
    while len(number) < 32:
        number = "0" + number
    octets = [number[:8], number[8:16], number[16:24], number[24:]]
    ip = str()
    for octet in octets:
        ip += str(int(octet, base=2))
        ip += "."
    
    return ip[:-1]


def ip_to_number(address):

    octets = address.split(".")
    address = str()
    
    for octet in octets:
        octet = bin(int(octet))[2:]
        while len(octet) < 8: octet = "0" + octet
        address += octet
            
    address = int(address, base=2)

    return [address]


def generate_targets_from_input(targets_input):

    if "/" in targets_input:
        targets = generate_targets_from_cidr(targets_input)

    else:
        targets = ip_to_number(targets_input)
    
    return targets


def generate_ports_from_input(ports_input):

    ports_extremes = ports_input.split("-")
    ports = list(range(int(ports_extremes[0]), int(ports_extremes[1]) + 1))
    
    return ports


def main():
    
    # endreço único, ou rede xxx.xxx.xxx.xxx/xx
    targets = generate_targets_from_input(sys.argv[1])

    # range de portas na forma xxxxx-yyyyy
    ports = generate_ports_from_input(sys.argv[2])

    scanner = PortScanner(targets, ports)
    scanner.scan_targets()


if __name__ == "__main__":
    main()