import argparse, sys
from reflector import utils

def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('mcast_addr', help='Multicast group to join')
    parser.add_argument('mcast_port', help='Multicast port', type=int)
    parser.add_argument('ucast_addr', help='Unicast address to send to')
    parser.add_argument('ucast_port', help='Unicast port', type=int)

    return parser.parse_args()
    
if __name__ == '__main__':
    options = get_opts()

    recv_mcast = utils.Receiver(options.mcast_addr, options.mcast_port)
    send_ucast = utils.Sender(options.ucast_addr, options.ucast_port)
    recv_mcast.start()

    try:
        while True:
            data = recv_mcast.receive()
            print("% data received" % recv_mcast.count)
            send_ucast.send(data)
    except KeyboardInterrupt:
        print('\nClosing Sockets')
    finally:
        send_ucast.stop()
        recv_mcast.stop()
        sys.exit(0)
       