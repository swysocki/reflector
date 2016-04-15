import socket
IP_ADDR = '192.168.2.55'

class Receiver:
    """ Joins a Multicast Group

    Receiver joins a specified Multicast Group with the intention of reflecting the
    traffic to a unicast address.

    Params:
        group (str): a dotted decimal (IPv4) address of the multicast group to
        join
        port (int): an integer representing the multicast port number

    """
    def __init__(self, group, port):
        self._MCAST_GRP = group
        self._MCAST_PORT = port
        self.rsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            
        host = IP_ADDR # We need a utility to get the interface address (netifaces)

        # sets the join address to the "host" var
        self.rsock.setsockopt(socket.SOL_IP, 
                              socket.IP_MULTICAST_IF, 
                              socket.inet_aton(host))

        membership_request = socket.inet_aton(self._MCAST_GRP) + socket.inet_aton(IP_ADDR)
        self.rsock.setsockopt(socket.IPPROTO_IP, 
                              socket.IP_ADD_MEMBERSHIP, 
                              membership_request)


    def start(self):
        self.rsock.bind((self._MCAST_GRP, self._MCAST_PORT))

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
        print('Sent %s bytes of data' % len(data))
        self.ssock.sendto(data, (self._UCAST_ADDR, self._UCAST_PORT))

