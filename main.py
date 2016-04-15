import argparse
from lib import net

def get_mcast_socket(args):
    return net.Receiver(args.mcast_addr, args.mcast_port) 

def get_ucast_socket(args):
    return net.Sender(args.ucast_addr, args.ucast_port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mcast_addr', help='Multicast group to join')
    parser.add_argument('mcast_port', help='Multicast port', type=int)
    parser.add_argument('ucast_addr', help='Unicast address to send to')
    parser.add_argument('ucast_port', help='Unicast port', type=int)

    args = parser.parse_args()

    recv_mcast = get_mcast_socket(args) 
    send_ucast = get_ucast_socket(args)
    recv_mcast.start()
    while True:
        data, address = recv_mcast.rsock.recvfrom(4096)
        print("% sent %s" % (address, len(data)))
        send_ucast.send(data)
