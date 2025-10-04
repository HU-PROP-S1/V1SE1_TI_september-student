# Server software for point-to-point WiFi on Pico W
# Simplified and inspired by this example: https://forum.core-electronics.com.au/t/pi-pico-w-to-pico-w-simple-communications/16188/15
import network, socket, time
from machine import Pin

led = Pin("LED", Pin.OUT)

ap = network.WLAN(network.AP_IF)
ap.config(essid="PICO_AP", password="pico1234")
ap.active(True)
while not ap.active():
    time.sleep(0.1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 9999))

while True:
    msg, addr = s.recvfrom(32)
    m = msg.decode().strip().upper()
    if m == "ON":  led.value(1)
    if m == "OFF": led.value(0)