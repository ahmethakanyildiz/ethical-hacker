import scapy.all as scapy
from scapy_http import http
import optparse

def get_user_input():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Enter Interface")
    (user_input,arguments) = parser.parse_args()
    if not user_input.interface:
        print("Please enter interface")
    return user_input

def listen_packets(interface):
    scapy.sniff(iface=interface,store=False,prn=analyze_packets)
    #prn is a callback function.

def analyze_packets(packet):
    #packet.show()
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)

user_input=get_user_input()
listen_packets(str(user_input.interface))