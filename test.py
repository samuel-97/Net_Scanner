from scapy.all import ARP

test = ARP()

ob = test.summary()

print(ob)