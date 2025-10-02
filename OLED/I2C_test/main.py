# I2C_test: scan for devices on the I2C bus
"""
Wil je testen of je je I2C apparaten goed hebt aangesloten? Dan kun je deze code gebruiken.
Het is een I2C scanner die alle aangesloten I2C apparaten detecteert en hun adres toont.
Je kunt deze code uitvoeren op een Raspberry Pi Pico W met MicroPython.
"""

# I2C Scanner MicroPython
from machine import Pin, SoftI2C

# With SoftI2C you can choose any combination of pins
i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
# Alternative if you need pull-up resistors on the I2C data and clock line
# i2c = SoftI2C(scl=Pin(9, Pin.PULL_UP),sda=Pin(8, Pin.PULL_UP))

print('I2C SCANNER')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:', len(devices))

  for device in devices:
    print("I2C hexadecimal address: ", hex(device))