import subprocess
import optparse
import re

def get_user_input():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change")
    parser.add_option("-m", "--mac", dest="mac_address", help="new mac address")
    return parser.parse_args()


def change_mac_address(interface, mac_address):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def control_mac_address(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig))
    if new_mac:
        return new_mac.group(0)
    else:
        return None


(user_inputs, arguments) = get_user_input()
change_mac_address(user_inputs.interface, user_inputs.mac_address)
finalized_mac=control_mac_address(str(user_inputs.interface))
if finalized_mac==user_inputs.mac_address:
    print("Mac address changed succesfully!")
else:
    print("Ops! There is a problem!")
