# avmap

Downloads weather METARs for a configuration set of airports, and then
displays color-coded weather codes on a string of WS2801 controlled
LEDs.  Inserting the LEDs onto a sectional chart provides for a
geo-referenced display of aviation weather.  The controlling computer
that downloads and decodes weather METARs is a Raspberry Pi, which
drives the LEDs via a SPI bus.

This project is a simplified set of code from John Marzulli's
categorical-sectional, which was in turn forked from Dylan Rush's
project of the same name.  Categorical-sectional is a great idea, but
the implementation was consuming nearly the entire capacity of the
Raspberry Pi Zero W's CPU, which was causing thermal stress and random
system lockups.

This version is simplified by removing non-WS2801 LED options,
removing rapid polling and blinking capability (weather is polled
every 15 minutes), and removing nighttime fading of the airport
weather status colors.  The resulting code is easy to understand and
readily runs on a Pi Zero without system lockups.

## Configure the Python Environment

Avmap runs on python3, and requires the following modules:

```
sudo pip3 install Adafruit-WS2801
```

## Configuration of Raspberry Pi

Install Raspbian per the instructions on the Raspberry Pi website.
You will need an SDHC card reader and a laptop on which to format
the SDHC card.

After installing and updating your Raspbian systemThe first time you set up the Raspberry Pi for controlling the LED
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

## Electronics Component BOM

I recommend the Raspberry Pi Zero W, which has two benefits: a) it is
cheap and small, and b) it does not suffer from WiFi instability,
which the Raspberry Pi 4 suffers from as of Q1 2020.  The downsides of
the Pi Zero W are that it is a limited CPU, which means slow install
installs and slow bootups.  Once the avmap app is running, the Pi Zero
has more than enough horsepower to continue running the application.

The code will run on a Raspberry Pi 4, but the hardware SPI driver on the Pi 4
is flakey as of Q1 2020, and it does not communicate properly with the
LED string. I will eventually recode with a software bitbang driver,
which presumably will run on any Pi version.

## Raspberry Pi 

## Soldering leads to control the LEDs



## Configuring displayed airports
