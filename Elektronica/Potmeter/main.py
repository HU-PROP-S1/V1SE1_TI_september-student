# Elektronica - Potentiometer Demo
from machine import Pin, ADC
from utime import sleep_ms

# Define the ADC GPIO pin for the potentiometer
POT_PIN = 26

# Initialize the ADC
adc = ADC(Pin(POT_PIN))

while True:
    val = adc.read_u16()
    print(val)
    sleep_ms(1000)
