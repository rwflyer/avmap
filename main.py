
import airport_list
import leds
import time

# Loop fetching observations every N minutes, then sleep to wait for next interval.
# The NeoPixel lights remain lit as long as power stays up, so no refreshing is
# needed.

DELAY_MINUTES = 60 * 15

def mainloop():
    airports = airport_list.AirportList()
    led_string = leds.LedString()
    led_string.clear_to_black()

    while True:
        airports.retrieve_metars()
        airports.render_metars(led_string)
        time.sleep(DELAY_MINUTES)


if __name__ == '__main__':
    mainloop()
