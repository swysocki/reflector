# reflector
Multicast to Unicast Reflector

## Integration tests
on sender
`# iperf -c 239.5.5.5 -u -p 3333 -T 32 `

on reflector
`# python3 main.py 239.5.5.5 3333 192.168.199.7 5155 -i eth1`

on receiver
`# iperf -s 192.168.199.7 -u -p 5155`