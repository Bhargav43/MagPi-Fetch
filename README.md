# [MagPi-Fetch](https://github.com/Bhargav43/MagPi-Fetch)
## Purpose :bulb:
The [MagPi](https://magpi.raspberrypi.org/)  is the official Raspberry Pi magazine. Written for the community, it is packed with Pi-themed projects, computing and electronics tutorials, how-to guides, and the latest community news and events.

The softcopies of these mags are open for everyone online. You can visit [Issues](https://magpi.raspberrypi.org/issues) section and [Books](https://magpi.raspberrypi.org/books) section of [magpi.raspberrypi.org](https://magpi.raspberrypi.org/) for downloading manually.

[**MagPi-Fetch**](https://github.com/Bhargav43/MagPi-Fetch) is a simple app designed for automating the process of downloading the mags from the website with few inputs rather than visiting individual pages and the respective download redirects.

## Base System's Configurations :wrench:
**Sno.** | **Name** | **Version/Config.**
-------: | :------: | :------------------
1 | Operating System | Windows 10 x64 bit
2 | Python | Version 3.7.0 x64 bit
3 | PyInstaller | Version 3.6
4 | IDE | Pyzo 4.10.2 x64 bit

_Recommendation: Except for Type of OS (Windows), other configurations doesn't matter even if you don't have Python in your system, if you are using the [`executable`](https://github.com/Bhargav43/MagPi-Fetch/blob/master/MagPi-Fetch.exe) directly. Try It._

## Requirements :heavy_exclamation_mark:
There aren't any mandates for this. Yet I recommend you to have the following.
1. Reliable internet connection as the downloads process in buffer.
1. Considerable space in the location of downloads.

By 31-May-2020,
* No. of Mags = 121
* Space Occupied = 2.58 GB
* Time Consumed = 30 mins. (approx.)

## Imported Modules :package:
Sn | **Module** | **Type** | **Version**
-: | :--------: | :------- | :----------
1 | os | *Built-in* | NA
2 | time | *Built-in* | NA
3 | re | *Built-in* | NA
4 | requests | *PyPI Installed* | 2.23.0
5 | requests_html | *PyPI Installed* | 0.10.0
6 | beautifulsoup4 | *PyPI Installed* | 4.9.1

