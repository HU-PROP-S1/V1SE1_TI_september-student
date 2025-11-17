# demo_matrix - demo code for LED matrix with MAX7219
"""
Demo code voor het testen van je LED matrix met de Pico W
 
Aansluiting is als volgt [LED Matrix naar Pico]:

 * VCC  pin naar VBUS (5V)
 * GND  pin naar GND
 * DIN  pin naar GPIO3
 * CS   pin naar GPIO5
 * CLK  pin naar GPIO2
"""
# Import MicroPython libraries
from machine import Pin, SPI
from time import sleep_ms

# Import de max7219 library - deze moet dus al op je pico staan. Is te vinden in de lib map.
import max7219

# Intialiseer SPI protocol
spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

# Instantieer matrix8x8 object. Met de laatste parameter geef je aan hoeveel matrices je hebt aangesloten.
display = max7219.Matrix8x8(spi, ss, 1)
display.brightness(10)  # Tussen 0 en 15
display.set_rotation(270)  # Zet de rotatie op 270 graden, dan is pixel (0,0) links bovenin.

# Clear the display.
display.fill(0)
display.show()

# Sleep for one second
sleep_ms(1000)

# Create pattern
arrow = [
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0]
]

# Show in different rotations
for rotation in [0, 90, 180, 270]:
    display.set_rotation(rotation)
    display.write_matrix(arrow)
    display.show()
    sleep_ms(1000)

# TODO:
#  - while-loop to repeat the animation
#  - lower brightness after first run
