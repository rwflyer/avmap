# avmap

Downloads weather METARs for a configuration set of airports, and then
displays color-coded weather codes on a string of WS2801 controlled
LEDs.  Inserting the LEDs onto a sectional chart provides for a
geo-referenced display of aviation weather.

## Configuration of Raspberry Pi

The first time you set up the Raspberry Pi for controlling the LED
string you must enable the SPI device:

```
sudo raspi-config
```

Select the Interfaces section, and enable the SPI bus.  Then verify
that the SPI bus device exists:

```
ls /dev
```

Observe that /dev/spidev0.0 exists.

## Soldering leads to control the LEDs


## Configuring displayed airports
