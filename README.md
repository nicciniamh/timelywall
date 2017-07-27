# Timely Wallpaper

Changes Wallpaper based on time of day and position of sun. Will work with Cinnamon and likely
Gnome and Unity. Maybe Mate too. 

## Wallpaper is changed for

* Night - whenever the sun is below the the horizon after local twilight
* Morning - During local twilight before noon. 
* Daytime - when the sun is visible
* Evening - During local twilight after noon. 

Configuration: An icon is placed in the system tray. It will, when clicked, bring up the configuration dialog. Configuration items are: 

* Night:    Path for Night Images
* Morning - Path for Monring Images
* Daytime - Path for Daytime Images
* Evening - Path for Evening Images
* Cycle Images: Set to allow image cycling else the first found image in each path will be used.
* Order: The sorting order for the image cycling (Name,Date,Random)
* Latitude/Longitude: Where you are in the world. (See notes below)
* Altitude: Your elevation. 
* Twilight Type: Civil, Nautical, Astronomical (See notes below)

## Notes
Latitude and Longitude can be in decimmal or deg:min:sec notation. 
Western longitudes and southern latitudes are negative
Return a string indicating night, morning, datime or evening. 
Examples:

Los Angeles, CA is 34.039714/-118.310327 or 34:02:22.3828/-118:18:37.136

Sydney, AU is -33.8688/151.2093 or -33:52:7.68/151:12:33.48

*Please see the ephem (PyPi) documentation (http://rhodesmill.org/pyephem/) for full
specifications of coordinates. 

Twlight is specified as Civil (-6 degrees) Nautical (-12 degrees) 
and Astronomical -18 degrees.

If using civil twilight:

It is night when the sun is below -6 degrees on the horizon.

It is morning when it is before noon and the sun is between -6 and 0 degrees on the horizon

it is after noon when the hour is >= 12 and the sun is greater than 0 degrees on the horizon

It is evening when it is after noon and the sun is between 0 and -6 degres on the horizon

