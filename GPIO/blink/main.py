# GPIO: LED blink
from machine import Pin
from utime import sleep_ms

gpio_pin = Pin(20, Pin.OUT)


def led_flash(led_pin, time_ms_on, time_ms_off):
    led_pin.value(1)
    # TODO: werk deze functie uit


# Example for a LED flashing once per second
while True:
    # TODO: vervang dit met een aanroep van led_flash met de juiste parameters
    gpio_pin.value(1)
    sleep_ms(500)
    gpio_pin.value(0)
    sleep_ms(500)
