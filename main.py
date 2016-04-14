from lib import net

if __name__ == '__main__':
    recv_mcast = net.Receiver('239.1.1.2', 1234)
    send_ucast = net.Sender('192.168.2.50', 1235)

    while True:
        data, address = recv_mcast.rsock.recvfrom(4096)
        print("% sent %s" % (address, len(data)))
        send_ucast.send(data)
