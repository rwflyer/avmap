
import metar
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


# Given an airport list of observations, render it to the NeoPixel lights
# based on the current observation and the offsets in the configuration data

PIXEL_COUNT = 25
SPI_PORT = 0
SPI_PORT_DEVICE = 0

colors = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'LOW': (255, 0, 255),
    'OFF': (0, 0, 0),
    'GRAY': (50, 50, 50),
    'YELLOW': (255, 255, 0),
    'DARK_YELLOW': (20, 20, 0),
    'WHITE': (255, 255, 255)
}

color_by_category = {
    metar.IFR: colors['RED'],
    metar.VFR: colors['GREEN'],
    metar.MVFR: colors['BLUE'],
    metar.LIFR: colors['LOW'],
    metar.SMOKE: colors['GRAY'],
    metar.INVALID: colors['OFF']
}

def setup_pixel_device():
    # hardware SPI connection on /dev/spidev0.0
    p = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_PORT_DEVICE))
    p.clear()
    p.show()

    [p.set_pixel(pixel, Adafruit_WS2801.RGB_to_color(0, 0, 0))
         for pixel in range(0, PIXEL_COUNT)]
    p.show()
    
    return p

pixels = None

def render_pixel(airport_offset, color):
    global pixels

    print('render_pixel: {} {}'.format(airport_offset, color))

    pixels.set_pixel(airport_offset, Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2]))
    pixels.show()
    
def color_for_category(cond):
    global color_by_category
    return color_by_category[cond]
    
def render_airports(airport_list):
    global pixels
    
    if pixels is None:
        pixels = setup_pixel_device()
    
    for obs in airport_list:
        metar = obs['metar']
        if metar is not None:
            color = color_for_category(metar.category())
        else:
            color = colors['OFF']

        render_pixel(obs['offset'], color)
        print('{}: {} {}'.format(obs['icao_code'], metar.category(), color))
