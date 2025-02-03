# Complete Spoofing Attacks Strategy
Spoofing strategy to bypass network access restrictions.

# Supported hardware
- Android phone (root)
- Openwrt Router
- Linux PC

# Steps
- Scan the network using any scanning tools that can fetch users dhcp ip and mac addresses.
> - Example:
```
Target IP: 10.0.0.110
Target MAC: D0:22:BE:28:40:BD
TARGET Hostname: Android
```
- Get the target ip and add it to the static ip settings of your device.
> - Android: `wifi static ip settings`
> - Openwrt: `luci interface`
> - Linux Pc: `Network Manager`
```
IP: 10.0.0.110
SUBNET: 255.255.255.240.0
GATEWAY: 10.0.0.1
DNS: 10.0.0.1
```
- Change your device Mac address (root) using any macchanger tools.
> - Openwrt: `vi /etc/config/wireless`
> - Linux Pc: `sudo nano /etc/NetworkManager/NetworkManager.conf`
```
Target Mac: D0:22:BE:28:40:BD
```
- Set your device hostname to the target Hostname.
> - Openwrt & Linux Pc: `sudo nano /etc/hostname`
```
Target Hostname: Android
```

- Refresh the Gateway 10.0.0.1 in the browser.

