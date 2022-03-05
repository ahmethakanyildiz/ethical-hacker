import scapy.all as scapy
import optparse

def get_user_input():
    parser = optparse.OptionParser()
    parser.add_option("-i","--ipaddress",dest="ip_address",help="Enter IP Address")
    (user_input,arguments) = parser.parse_args()
    if not user_input.ip_address:
        print("Please enter IP address")
    return user_input.ip_address

def scan_my_network(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #combining packets
    combined_packet=broadcast_packet/arp_request_packet
    #sending packets
    (answered_list,unanswered_list) = scapy.srp(combined_packet, timeout=1)
    answered_list.summary()

user_ip_address = get_user_input()
scan_my_network(user_ip_address)