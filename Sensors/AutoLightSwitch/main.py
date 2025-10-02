# Sensors - AutoLightSwitch
# Switch on an LED depending on the amount of light in the room

from machine import ADC, Pin
from utime import sleep_ms

LED_PIN = 15
ADC_PIN = 26

LOW_LIGHT_THRESHOLD = 50000 # onderdag, zonlicht

led = Pin(LED_PIN, Pin.OUT)
adc = ADC(Pin(ADC_PIN))

while True:
    value = adc.read_u16()
    # Debug
    print(f"adc_value = {value}")
    if value < LOW_LIGHT_THRESHOLD:
        led.value(1)
    else:
        led.value(0)
    sleep_ms(5000)
