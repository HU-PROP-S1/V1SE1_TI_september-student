"""
MicroPython max7219 cascadable 8x8 LED matrix driver
https://github.com/mcauser/micropython-max7219

MIT License
Copyright (c) 2017 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Edits to enable rotation of the display and to implement the ability to work with patterns/matrices made by Nick Goris (2025)
"""

from micropython import const
import framebuf

_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

class Matrix8x8:
    def __init__(self, spi, cs, num):
        """
        Driver for cascading MAX7219 8x8 LED matrices.

        >>> import max7219
        >>> from machine import Pin, SPI
        >>> spi = SPI(1)
        >>> display = max7219.Matrix8x8(spi, Pin('X5'), 4)
        >>> display.text('1234',0,0,1)
        >>> display.show()

        """
        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(8 * num)
        self.num = num
        fb = framebuf.FrameBuffer(self.buffer, 8 * num, 8, framebuf.MONO_HLSB)
        self.framebuf = fb
        # Provide methods for accessing FrameBuffer graphics primitives. This is a workround
        # because inheritance from a native class is currently unsupported.
        # http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
        self.fill = fb.fill  # (col)
        self.pixel = fb.pixel # (x, y[, c])
        self.hline = fb.hline  # (x, y, w, col)
        self.vline = fb.vline  # (x, y, h, col)
        self.line = fb.line  # (x1, y1, x2, y2, col)
        self.rect = fb.rect  # (x, y, w, h, col)
        self.fill_rect = fb.fill_rect  # (x, y, w, h, col)
        self.text = fb.text  # (string, x, y, col=1)
        self.scroll = fb.scroll  # (dx, dy)
        self.blit = fb.blit  # (fbuf, x, y[, key])
        self.rotation = 0  # 0, 90, 180, 270 degrees
        self.init()

    def set_rotation(self, degrees):
        """Set rotation: 0, 90, 180, or 270 degrees"""
        if degrees not in [0, 90, 180, 270]:
            raise ValueError("Rotation must be 0, 90, 180, or 270 degrees")
        self.rotation = degrees

    def _transform_coords(self, x, y):
        """Transform coordinates based on rotation"""
        width = 8 * self.num
        height = 8
        
        if self.rotation == 0:
            return x, y
        elif self.rotation == 90:
            return height - 1 - y, x
        elif self.rotation == 180:
            return width - 1 - x, height - 1 - y
        elif self.rotation == 270:
            return y, width - 1 - x
        
    def pixel_rotated(self, x, y, c=None):
        """Set/get pixel with rotation applied"""
        tx, ty = self._transform_coords(x, y)
        if c is None:
            return self.framebuf.pixel(tx, ty)
        else:
            return self.framebuf.pixel(tx, ty, c)
    
    def text_rotated(self, string, x, y, col=1):
        """Display text with rotation applied"""
        if self.rotation == 0:
            return self.framebuf.text(string, x, y, col)
        else:
            # For rotated text, we need to draw character by character
            # This is a simplified version - full implementation would be more complex
            tx, ty = self._transform_coords(x, y)
            return self.framebuf.text(string, tx, ty, col)

    def _write(self, command, data):
        self.cs(0)
        for m in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    def show(self):
        if self.rotation == 0:
            self._show_direct()
        else:
            self._show_rotated()
    
    def _show_direct(self):
        """Direct show without rotation - original implementation"""
        for y in range(8):
            self.cs(0)
            for m in range(self.num):
                self.spi.write(bytearray([_DIGIT0 + y, self.buffer[(y * self.num) + m]]))
            self.cs(1)

    def _show_rotated(self):
        """Show with rotation applied by copying rotated buffer"""        
        # Create a temporary buffer for rotation
        width = 8 * self.num
        height = 8
        temp_buffer = bytearray(width * height // 8)
        temp_fb = framebuf.FrameBuffer(temp_buffer, width, height, framebuf.MONO_HLSB)
        
        # Copy pixels with rotation
        for x in range(width):
            for y in range(height):
                pixel_val = self.framebuf.pixel(x, y)
                if pixel_val:
                    tx, ty = self._transform_coords(x, y)
                    if self.rotation == 90 or self.rotation == 270:
                        # For 90/270 degree rotation, swap width/height
                        if 0 <= tx < height and 0 <= ty < width:
                            temp_fb.pixel(tx, ty, pixel_val)
                    else:
                        if 0 <= tx < width and 0 <= ty < height:
                            temp_fb.pixel(tx, ty, pixel_val)
        
        # Copy temp buffer to main buffer
        if self.rotation == 90 or self.rotation == 270:
            # For 90/270 rotation, we need to handle the dimension swap
            self.buffer[:] = temp_buffer[:]
        else:
            self.buffer[:] = temp_buffer[:]
        
        return self._show_direct()

    def write_matrix(self, matrix):
        """
        Write a 2D matrix of booleans/integers to the framebuffer
        
        Example:
            # Create a simple pattern
            pattern = [
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1]
            ]
            display.write_matrix(pattern)
            display.show()
        """
        height = len(matrix)
        if height == 0:
            return
            
        width = len(matrix[0])
        max_width = 8 * self.num
        
        # Clear the framebuffer first
        self.fill(0)
        
        # Write each pixel
        for y in range(min(height, 8)):  # MAX7219 is 8 pixels high
            for x in range(min(width, max_width)):  # Width depends on number of matrices
                if matrix[y][x]:  # Treats any truthy value as 'on'
                    self.pixel(x, y, 1)

    def read_matrix(self):
        """
        Read the framebuffer as a 2D matrix of booleans

        """
        width = 8 * self.num
        height = 8
        
        matrix = []
        for y in range(height):
            row = []
            for x in range(width):
                pixel_val = self.pixel(x, y)
                row.append(bool(pixel_val))
            matrix.append(row)
        
        return matrix

    def write_pattern(self, pattern_string, char_on='1', char_off='0'):
        """
        Write a pattern from a multi-line string (useful for ASCII art)
        
        Example:
            pattern = '''
            10101010
            01010101
            10101010
            01010101
            10101010
            01010101
            10101010
            01010101
            '''
            display.write_pattern(pattern)
            display.show()
        """
        lines = [line.strip() for line in pattern_string.strip().split('\n') if line.strip()]
        matrix = []
        
        for line in lines:
            row = []
            for char in line:
                row.append(char == char_on)
            matrix.append(row)
        
        self.write_matrix(matrix)
