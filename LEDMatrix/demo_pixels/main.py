"""
Demo code voor het testen van je LED matrix met de Pico W
 
Aansluiting is als volgt [LED Matrix naar Pico]:

 * VCC  pin naar VBUS (5V)
 * GND  pin naar GND
 * DIN  pin naar GPIO3
 * CS   pin naar GPIO5
 * CLK  pin naar GPIO2
"""
# Import MicroPython libraries time
from machine import Pin, SPI
import time

# Import de max7219 library - deze moet dus al op je pico staan. Is te vinden in de lib map.
import max7219

#Intialiseer SPI protocol
spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

# Instantieer matrix8x8 object. Met de laatste parameter geef je aan hoeveel matrices je hebt aangesloten.
display = max7219.Matrix8x8(spi, ss, 1)
display.brightness(10) # Tussen 0 en 15
display.set_rotation(270)  # Zet de rotatie op 270 graden, dan is pixel (0,0) links bovenin.

#Clear the display.
display.fill(0)
display.show()

#sleep for one one seconds
time.sleep(1)

# Unconditionally execute the loop
def main():
    while True:
        for x in range(8):
            for y in range(8):
                # Clear the display
                display.fill(0)
                
                # Set a pixel at (x, y) to white
                display.pixel(x, y, 1)
                
                # Show the display
                display.show()
                
                # Set the Scrolling speed. Here it is 100mS.
                time.sleep(0.1)
        print(dir(display.framebuf.FrameBuffer))  # Debugging output to see available methods

if __name__ == "__main__":
    main()
 
