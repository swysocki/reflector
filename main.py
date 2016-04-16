import argparse
from lib import net

def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('mcast_addr', help='Multicast group to join')
    parser.add_argument('mcast_port', help='Multicast port', type=int)
    parser.add_argument('ucast_addr', help='Unicast address to send to')
    parser.add_argument('ucast_port', help='Unicast port', type=int)

    return parser.parse_args()
    
def get_mcast_socket(options):
    return net.Receiver(options.mcast_addr, options.mcast_port) 

def get_ucast_socket(options):
    return net.Sender(options.ucast_addr, options.ucast_port)

if __name__ == '__main__':
    options = get_opts()

    recv_mcast = get_mcast_socket(options) 
    send_ucast = get_ucast_socket(options)
    recv_mcast.start()

    while True:
        data, address = recv_mcast.rsock.recvfrom(65536)
        print("% sent %s" % (address, len(data)))
        send_ucast.send(data)
