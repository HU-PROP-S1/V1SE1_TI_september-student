from machine import Pin, SoftI2C # SoftI2C is een softwarematige I2C implementatie, trager dan hardwarematig
from ssd1306 import SSD1306_I2C
import time

WIDTH =128 
HEIGHT= 64

i2c=SoftI2C(scl=Pin(5, Pin.PULL_UP),sda=Pin(4, Pin.PULL_UP))
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

def main():
    while True:
        oled.fill(0)
        oled.text("Hallo Wereld", 0, 0)
        oled.text("Spelen met hardware", 0, 40)
        oled.show()
        time.sleep(1)
        oled.fill(0)
        for x in range(0, 128, 8):
            for y in range(0, 64, 8):
                if y%16 == 0:
                    oled.rect(x, y, 8, 8, 1)
                else:
                    oled.ellipse(x + 4, y + 4, 4, 4, 1)
                oled.show()
                time.sleep(0.1)
                oled.fill(0)

if __name__ == "__main__":
    main()
