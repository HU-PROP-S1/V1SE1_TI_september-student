"""
HelloWorld is het eerste dat elke programmeur leert; het printen van de tekst 'Hello World' naar de console.
Als je op een microcontroller werkt is dit vaak lastiger - je hebt geen scherm, en ook niet altijd een console.
In plaats daarvan is de Hello World in de embedded wereld het laten knipperen van een LED.
Gelukkig heeft onze Pi Pico een LED ingebouwd, die gebruiken wij hier ook.

Gebruik deze code om te testen of je je Pico en ontwikkelomgeving goed hebt opgezet.
Verwacht resultaat: de LED op je Pico gaat steeds één seconde aan, dan één seconde uit. Herhaal oneindig.
"""

from machine import Pin
import utime

led = Pin("LED", Pin.OUT)

while True:
    led.toggle()  # Toggle the LED state
    utime.sleep(1)  # Wait for 1 second
