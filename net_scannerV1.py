from scapy.all import ARP, Ether, srp
import json
import os

# run ip tool to find network address
os.system("ip -j r > ipconfig.json")


# open json file and extract netmask as variable target_ip
file = open("/home/samuelrodier/Repos/Network_Scanner/ipconfig.json")

js = json.load(file)
file.close()
target_ip = js[2]['dst']

# IP Address for the destination
# create ARP packet
arp = ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# stack them
packet = ether/arp

result = srp(packet, timeout=3, verbose=1)[0]

# a list of clients, we will fill this in the upcoming loop
clients = []

for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))