#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.nodelib import NAT

# MiniFlix origin server, running inside the VM
HOST_IP = "127.0.0.1"

# Outbound interface on the VM (check with: ip addr)
INET_IF = "enp0s1"

class MiniFlixTopo(Topo):
    def build(self, inetIntf=INET_IF, subnet='10.0.0.0/24'):

        # Switch
        s1 = self.addSwitch('s1')

        # NAT node (root namespace)
        nat = self.addNode(
            'nat0',
            cls=NAT,
            ip='10.0.0.1/24',
            inNamespace=False,
            inetIntf=inetIntf,
            subnet=subnet
        )
        self.addLink(nat, s1)

        # Bad client
        h1 = self.addHost('h1')
        self.addLink(h1, s1,
                     cls=TCLink, bw=3, delay='80ms', loss=1)

        # Good client
        h2 = self.addHost('h2')
        self.addLink(h2, s1,
                     cls=TCLink, bw=50, delay='10ms', loss=0)


def run():
    topo = MiniFlixTopo()
    net = Mininet(topo=topo, controller=None, link=TCLink)
    net.start()

    print("\nConfiguring nodes...\n")

    # Retrieve nodes
    h1 = net.get('h1')
    h2 = net.get('h2')
    s1 = net.get('s1')
    nat = net.get('nat0')

    # --- SWITCH FIX ---
    # Bring up all switch ports (eth1, eth2, eth3)
    for i in range(1, 4):
        s1.cmd(f"ip link set s1-eth{i} up")

    # Assign IP to bridge
    s1.cmd("ip addr flush dev s1")
    s1.cmd("ip addr add 10.0.0.1/24 dev s1")
    s1.cmd("ip link set s1 up")

    # --- HOST CONFIG ---
    # h1
    h1.cmd("ip addr flush dev h1-eth0")
    h1.cmd("ip addr add 10.0.0.11/24 dev h1-eth0")
    h1.cmd("ip link set h1-eth0 up")
    h1.cmd("ip route add default via 10.0.0.1")

    # h2
    h2.cmd("ip addr flush dev h2-eth0")
    h2.cmd("ip addr add 10.0.0.12/24 dev h2-eth0")
    h2.cmd("ip link set h2-eth0 up")
    h2.cmd("ip route add default via 10.0.0.1")

    # --- NAT CONFIG ---
    nat.cmd("sysctl -w net.ipv4.ip_forward=1")
    nat.cmd(f"iptables -t nat -A POSTROUTING -o {INET_IF} -j MASQUERADE")
    nat.cmd("iptables -A FORWARD -i s1-eth0 -j ACCEPT")
    nat.cmd("iptables -A FORWARD -o s1-eth0 -j ACCEPT")

    print("MiniFlix Mininet topology is running.")
    print("From h1/h2 terminals, try:")
    print(f"  curl -I http://{HOST_IP}:8080")
    print(f"  curl -I http://{HOST_IP}:8080/hls/rtmp.m3u8 (when streaming)")
    print(f"  ping {HOST_IP}\n")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
