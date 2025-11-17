# demo_text - demo code for LED matrix with MAX7219
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

# Definiëer bericht
scrolling_message = "HALLO WERELD!"
length = len(scrolling_message)

# Bereken het aantal kolommen van het bericht
column = (length * 8)

# Clear the display.
display.fill(0)
display.show()
display.set_rotation(270)  # Zet de rotatie op 270 graden, dan worden letters van links naar rechts getoond.

# Sleep for one second
sleep_ms(1000)


def main():
    # Unconditionally execute the loop
    while True:
        for i in range(32, -column, -1):
            # Clear the display
            display.fill(0)
            # Write the scrolling text in to frame buffer
            display.text(scrolling_message, i, 0, 1)
            # Show the frame buffer content on the display
            display.show()
            # Here we wait for 50ms. This is the scrolling speed.
            sleep_ms(50)


if __name__ == "__main__":
    main()
