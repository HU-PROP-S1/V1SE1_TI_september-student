# Client software for point-to-point WiFi on Pico W
# Simplified and inspired by this example: https://forum.core-electronics.com.au/t/pi-pico-w-to-pico-w-simple-communications/16188/15
import network, socket, time
from machine import Pin

BTN_PIN = 15
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("PICO_AP", "pico1234")
while not sta.isconnected():
    time.sleep(0.1)

server_ip = "192.168.4.1"  # standaard IP van Pico AP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

last = btn.value()
led_state = False

while True:
    v = btn.value()
    if v != last and v == 0:           # falling edge = knop ingedrukt
        led_state = not led_state
        s.sendto(b"ON" if led_state else b"OFF", (server_ip, 9999))
    last = v
    time.sleep(0.02)  # debounce