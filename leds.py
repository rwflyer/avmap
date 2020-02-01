
#import json
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

#
# Publishes an abstraction for an LED string. Reads configuration for the LED string.
#

PIXEL_COUNT = 25
SPI_PORT = 0
SPI_PORT_DEVICE = 0

USE_HARDWARE_DEVICE = True

class LedString(object):
    def __init__(self):
        # TODO: Replace with configuration file
        if USE_HARDWARE_DEVICE:
            self.hardware_device = True
            self.pixel_count = PIXEL_COUNT
            # hardware SPI connection on /dev/spidev0.0
            self.hwdevice = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_PORT_DEVICE))
        else:
            assert False

    def clear_to_black(self):
        if self.hardware_device:
            self.hwdevice.clear()
            self.hwdevice.show()
        else:
            assert False

    def set_pixel(self, offset, rgb_color):
        if self.hardware_device:
            # print('render_pixel: {} {}'.format(offset, rgb_color))
            
            self.hwdevice.set_pixel(offset, Adafruit_WS2801.RGB_to_color(rgb_color[0], rgb_color[1], rgb_color[2]))
            self.hwdevice.show()
        else:
            assert False
