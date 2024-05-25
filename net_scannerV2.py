# V2 of the netscanner will include a Mac Address lookup API. Hopefully this will allow me to 
    # figure out the device type connected to the network. 

from scapy.all import ARP, Ether, srp
import json
import os
import requests

# run ip tool to find network address
os.system("ip -j r > '/home/samuelrodier/Repos/Networking_Projects/Network_Scanner/ipconfig.json")


# open json file and extract netmask as variable target_ip
file = open("/home/samuelrodier/Repos/Networking_Projects/Network_Scanner/ipconfig.json")

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
    # each response will also send an api request to look up the company that produced the network
        # card for the device
    
    URL = "http://www.macvendorlookup.com/api/v2/"  # free api-endpoint
    
    # send request and saving the response as response object
    
    try: 
        r = requests.get(URL+str(received.hwsrc))
        response = r.json()
    
        company = response[0]['company']
        clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'manufacturer':company})
    except json.decoder.JSONDecodeError:
        idk = 'unknown'
        clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'manufacturer':idk})
        
# for each response, append ip and mac address to `clients` list

# print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC"+ " "*19 + "Manufacturer")
for client in clients:
    print("{:16}    {}     {}".format(client['ip'], client['mac'], client['manufacturer']))