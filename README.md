# avmap
The first time you set up the Raspberry Pi for controlling the LED
string you must enable the SPI device:

sudo raspi-config

Select Interfaces
Enable the SPI bus.

Verify that the SPI bus device exists:

ls /dev

Observe that /dev/spidev0.0 exists.

