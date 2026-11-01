# send.py by sd, tested on A07

import usb.core
import usb.util
import sys

dev = usb.core.find(idVendor=0x04e8, idProduct=0x685d)
if dev is None:
    print("Device not found.")
    sys.exit(1)

for cfg in dev:
    for intf in cfg:
        try:
            if dev.is_kernel_driver_active(intf.bInterfaceNumber):
                dev.detach_kernel_driver(intf.bInterfaceNumber)
        except Exception:
            pass

dev.set_configuration()
cfg = dev.get_active_configuration()
intf = cfg[(1, 0)]

ep_in = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
ep_out = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

print("[*] Sending DVIF (4 bytes) + ZLP...")
try:
    ep_out.write(b"DVIF") # Send the command
    ep_out.write(b"")     # Send Zero Length Packet to finish the transfer
    print("[+] Data sent. Waiting for response...")
    ret = ep_in.read(512, timeout=3000)
    print("[+] Response:", bytes(ret))
except usb.core.USBError as e:
    print("[!] USB Error:", e)

print("\n[*] Done.")
