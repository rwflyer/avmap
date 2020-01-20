
import airport_list
import metar
import render

import time

# Loop fetching observations every N minutes, then sleep to wait for next interval.
# The NeoPixel lights remain lit as long as power stays up, so no refreshing is
# needed.

DELAY_MINUTES = 60 * 15

def mainloop():
    airport_list.read_airports()

    while True:
        airport_list.retrieve_metars()
        render.render_airports(airport_list.metar_store)
        time.sleep(DELAY_MINUTES)


if __name__ == '__main__':
    mainloop()
