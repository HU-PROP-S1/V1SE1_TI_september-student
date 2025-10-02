// Demo to control a sprite with a variable resistor (100K potentiometer)
from machine import Pin, SoftI2C, ADC  # SoftI2C is software I2C; hardware I2C kan ook (sneller)
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB
import time
import math

WIDTH  = 128
HEIGHT = 64

# I2C en OLED
i2c  = SoftI2C(scl=Pin(5, Pin.PULL_UP), sda=Pin(4, Pin.PULL_UP))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Potmeter op ADC0 (GP26)
adc_x = ADC(26)

# (Optioneel) tweede potmeter voor Y:
# adc_y = ADC(27)  # GP27/ADC1

# Klein 8x8 sprite (TI byte array)
# Bits zijn MONO_HLSB (1 = wit pixel)
# Design your own: https://xantorohara.github.io/led-matrix-editor
SPRITE_W = 8
SPRITE_H = 8
sprite_bytes = bytearray([
    0b00000000,
    0b00000000,
    0b01110100,
    0b00100100,
    0b00100100,
    0b00100100,
    0b00000000,
    0b00000000
])
sprite = FrameBuffer(sprite_bytes, SPRITE_W, SPRITE_H, MONO_HLSB)

def read_adc_scaled(adc, out_max):
    """Lees ADC (0..65535) en schaal naar 0..out_max (int). Met eenvoudige oversampling."""
    s = 0
    for _ in range(8):  # klein beetje ruis-averaging
        s += adc.read_u16()
    val = s // 8
    return (val * out_max) // 65535

def clamp(v, lo, hi):
    return lo if v < lo else (hi if v > hi else v)

def main():
    # EMA (exponential moving average) voor soepele X-positie
    alpha = 0.25
    x_norm = 0.0  # genormaliseerd 0..1 voor X
    # Y: rustig op/neer bewegen (sinus). Pas speed aan naar smaak.
    t0 = time.ticks_ms()
    y_speed = 0.9  # Hz (golven per seconde)

    # (Optioneel) vast raster op achtergrond:
    show_grid = False

    while True:
        # Meet potmeter en filter
        raw_x = read_adc_scaled(adc_x, 1000)  # hogere resolutie vóór normaliseren
        x_target = raw_x / 1000.0             # 0..1
        x_norm = (1 - alpha) * x_norm + alpha * x_target

        # Schaal naar pixelpositie met marge voor spritebreedte
        x = int(x_norm * (WIDTH - SPRITE_W))
        x = clamp(x, 0, WIDTH - SPRITE_W)

        # Y bepalen: sinusbeweging (of gebruik een tweede potmeter)
        ms = time.ticks_diff(time.ticks_ms(), t0)
        t  = ms / 1000.0  # sec
        # (Als je een tweede potmeter gebruikt, vervang onderstaande 3 regels door:)
        # y = read_adc_scaled(adc_y, HEIGHT - SPRITE_H)
        amplitude = (HEIGHT - SPRITE_H) / 2
        y_center = (HEIGHT - SPRITE_H) / 2
        y = int(y_center + amplitude * math.sin(2 * math.pi * y_speed * t))
        y = clamp(y, 0, HEIGHT - SPRITE_H)

        # Tekenen
        oled.fill(0)

        if show_grid:
            for gx in range(0, WIDTH, 8):
                oled.rect(gx, 0, 1, HEIGHT, 1)
            for gy in range(0, HEIGHT, 8):
                oled.rect(0, gy, WIDTH, 1, 1)

        # Titelregel (klein, kost weinig)
        oled.text("Potmeter = X", 0, 0)

        # Sprite “blitten”
        oled.blit(sprite, x, y)

        oled.show()

        # ~30 FPS-ish; pas aan naar smaak.
        time.sleep(0.03)

if __name__ == "__main__":
    main()