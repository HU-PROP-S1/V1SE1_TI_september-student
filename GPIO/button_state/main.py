# GPIO: Button state
from machine import Pin
from utime import sleep_ms

button_pin = Pin(19, Pin.IN, pull=Pin.PULL_DOWN)

while True:
    state = button_pin.value()
    # TODO: print state to the MicroPython console
    sleep_ms(1000)
