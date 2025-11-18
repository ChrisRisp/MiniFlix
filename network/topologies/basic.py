#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.nodelib import NAT

HOST_IP = "192.168.1.100"      # e.g. "192.168.1.37"

# Outbound interface in the VM 
INET_IF = "enp0s1"       # e.g. "enp0s3" or "eth0"

class MiniFlixTopo(Topo):
    def build(self, inetIntf=INET_IF, subnet='10.0.0.0/24'):
        s1 = self.addSwitch('s1')

        # NAT node in the *root* namespace
        nat = self.addNode('nat0',
                           cls=NAT,
                           ip='10.0.0.1/24',
                           inNamespace=False,
                           inetIntf=inetIntf,
                           subnet=subnet)
        self.addLink(nat, s1)

        # Bad network client
        h1 = self.addHost('h1',
                          ip='10.0.0.11/24',
                          defaultRoute='via 10.0.0.1')
        self.addLink(h1, s1,
                     cls=TCLink,
                     bw=3, delay='80ms', loss=1)

        # Good network client
        h2 = self.addHost('h2',
                          ip='10.0.0.12/24',
                          defaultRoute='via 10.0.0.1')
        self.addLink(h2, s1,
                     cls=TCLink,
                     bw=50, delay='10ms', loss=0)

def run():
    topo = MiniFlixTopo()
    net = Mininet(topo=topo, controller=None, link=TCLink)
    net.start()

    print("MiniFlix Mininet topology is running.")
    print("From h1/h2 terminals, try:")
    print(f"  curl -I http://{HOST_IP}:8080")
    print(f"  curl -I http://{HOST_IP}:8080/hls/rtmp.m3u8  (when streaming)")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
