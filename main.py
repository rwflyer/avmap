
import airport_list
import leds
import time

# Loop fetching observations every N minutes, then sleep to wait for next interval.
# The NeoPixel lights remain lit as long as power stays up, so no refreshing is
# needed.

REFRESH_MINUTES = 60 * 15



def mainloop():
    airports = airport_list.AirportList()
    led_string = leds.LedString()
    led_string.clear_to_black()

    delay_sequence = [0.5 * 60, 1 * 60, 2 * 60, 5 * 60, 10 * 60, 15 * 60]
    sequence_num = 0
    
    while True:
        valid = airports.retrieve_metars()
        if valid:
            airports.render_metars(led_string)
            sequence_num = 0
            delay = REFRESH_MINUTES
        else:
            if sequence_num >= len(delay_sequence):
                delay = delay_sequence[-1]
            else:
                delay = delay_sequence[sequence_num]
                sequence_num += 1
                
        time.sleep(delay)


if __name__ == '__main__':
    mainloop()
