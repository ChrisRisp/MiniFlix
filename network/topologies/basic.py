#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

# Set IP address where Docker exposes MiniFlix
HOST_IP = "127.0.0.1"

# Set this to the outbound interface on the host
# If you want Mininet to talk via your LAN: use e.g. "eth0" / "enp3s0" / "wlp0s20f3"
OUT_IF = "docker0"           

class MiniFlixBasic(Topo):
    def build(self):
        s1 = self.addSwitch('s1')

        h1 = self.addHost('h1', ip='10.0.0.11/24')
        self.addLink(h1, s1,
                     cls=TCLink,
                     bw=3, delay='80ms', loss=1)

        h2 = self.addHost('h2', ip='10.0.0.12/24')
        self.addLink(h2, s1,
                     cls=TCLink,
                     bw=50, delay='10ms', loss=0)

        nat = self.addHost('nat0', ip='10.0.0.1/24')
        self.addLink(nat, s1)

def run():
    topo = MiniFlixBasic()
    net = Mininet(topo=topo, controller=None, link=TCLink)
    net.start()

    nat = net.get('nat0')

    # NAT so h1/h2 can reach HOST_IP and thus Docker
    nat.cmd(f'iptables -t nat -A POSTROUTING -o {OUT_IF} -j MASQUERADE')
    nat.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')

    for name in ['h1', 'h2']:
        host = net.get(name)
        host.cmd('ip route add default via 10.0.0.1')

    print("MiniFlix Mininet topology is running.")
    print("From h1/h2 terminals, try:")
    print(f"  curl -I http://{HOST_IP}:8080/hls/rtmp.m3u8")
    print(f"  ffmpeg -i http://{HOST_IP}:8080/hls/rtmp.m3u8 -t 5 -f null -")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
