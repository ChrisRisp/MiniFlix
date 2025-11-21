#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

class TestTopo(Topo):
    def build(self):
        # Single switch
        s1 = self.addSwitch('s1')

        # Single host, no IP yet – we'll set it manually
        h1 = self.addHost('h1')

        self.addLink(h1, s1)

def run():
    topo = TestTopo()
    net = Mininet(topo=topo, controller=None)
    net.start()

    h1 = net.get('h1')

    # Configure h1 and s1 explicitly
    print(h1.cmd("ip addr add 10.0.0.11/24 dev h1-eth0"))
    print(h1.cmd("ip link set h1-eth0 up"))
    print(h1.cmd("ip route add default via 10.0.0.1"))

    # Give the bridge an IP
    print(net.get('s1').cmd("ip addr add 10.0.0.1/24 dev s1"))
    print(net.get('s1').cmd("ip link set s1 up"))

    print("From h1, try:")
    print("  ping 10.0.0.1")

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    run()
