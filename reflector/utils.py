import socket, os

def get_ip_addr():
    """ Retrieves Interface IPv4 Address
    
    Uses an Linux-specific OS call to parse the IP address.  Creates a list of
    strings if multiple interfaces are present.  Currently only uses the first
    address found.  This only works on systems with interfaces prefixed with
    'ethX' e.g. Debian
    
    returns:
        ips[0] (str): a string representing the first IPv4 address found

    """
    out = os.popen("ip a s | grep 'inet.*eth[0-99]' | cut -f6 -d' ' | sed 's/\/.*//'")
    ips = out.read().split()
    return ips[0]
    

class Receiver:
    """ Joins a Multicast Group

    Receiver joins a specified Multicast Group with the intention of reflecting the
    traffic to a unicast address.

    Properties:
        _MCAST_GRP (str): a dotted decimal (IPv4) address of the multicast group to
        join
        _MCAST_PORT (int): an integer representing the multicast port number
        count (int): bytes received on socket
        rsock (obj): Python socket object
        
    """
    def __init__(self, group, port):
        self._MCAST_GRP = group
        self._MCAST_PORT = port
        self.count = 0
        self.rsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
       
        host = get_ip_addr()

        self.rsock.setsockopt(socket.SOL_IP, 
                              socket.IP_MULTICAST_IF, 
                              socket.inet_aton(host))

        membership_request = socket.inet_aton(self._MCAST_GRP) + socket.inet_aton(host)
        self.rsock.setsockopt(socket.IPPROTO_IP, 
                              socket.IP_ADD_MEMBERSHIP, 
                              membership_request)

    def start(self):
        self.rsock.bind((self._MCAST_GRP, self._MCAST_PORT))

    def receive(self):
        data, address = self.rsock.recvfrom(65536)
        self.count += len(data)
        return data
        
    def stop(self):
        self.rsock.close()


class Sender:
    """
    Sends unicast data

    Sender 'reflects' the Receiver's data by opening a unicast UDP socket and
    sending any incoming bytes to the destination address

    Params:
        addr (str): a dotted decimal (IPv4) addres of the unicast
        destiation
        port (int): an integer representing the unicast port number

    """ 
    def __init__(self, address, port):
        self._UCAST_ADDR = address
        self._UCAST_PORT = port
        self.ssock = socket.socket(socket.AF_INET, 
                                   socket.SOCK_DGRAM,
                                   socket.IPPROTO_UDP)
                                   
    def send(self, data):
        self.ssock.sendto(data, (self._UCAST_ADDR, self._UCAST_PORT))
    
    def stop(self):
        self.ssock.close()

