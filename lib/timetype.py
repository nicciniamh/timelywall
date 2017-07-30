#
# Timely Wallpaper Changer
# Copyright 2017 Nicole Stevens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import debug, datetime, ephem, math
twilightDegrees = {'civil': -6, 'nautical': -12, 'astronomical': -18}
def getTimeType(latitude, longitude, altitude, twilight='civil'):
    '''
    get the time of day time (night,morning,day,evening) based on lat/lon/alt
    Latitude and Longitude can be in decimmal or deg:min:sec notation. 
    Western longitudes and southern latitudes are negative
    Return a string indicating night, morning, datime or evening. 
    Example:
        Los Angeles, CA is 34.039714/-118.310327 or 34:02:22.3828/-118:18:37.136
        Sydney, AU is -33.8688/151.2093 or -33:52:7.68/151:12:33.48

        Please see the ephem (PyPi) documentation (http://rhodesmill.org/pyephem/) for full
        specifications of coordinates. 

    Twlight is specified as Civil (-6 degrees) Nautical (-12 degrees) 
    and Astronomical -18 degrees.

    If using civil twilight:
    It is night when the sun is below -6 degrees on the horizon.
    It is morning when it is before noon and the sun is between -6 and 0 degrees on the horizon
    it is after noon when the hour is >= 12 and the sun is greater than 0 degrees on the horizon
    It is evening when it is after noon and the sun is between 0 and -6 degres on the horizon
    '''
    if not twilight.lower() in twilightDegrees:
        raise ValueError('Twilight must be one of',', '.join(list(twilightDegrees.keys())))
    debug.debug('Calculating for {}/{} elevation {}'.format(latitude,longitude,altitude))
    debug.debug('{} twilight is {} degrees below horizon'.format(twilight,abs(twilightDegrees[twilight.lower()])))
    sun = ephem.Sun()
    observer = ephem.Observer()
    observer.lat = latitude
    observer.lon = longitude
    try:
        observer.elevation = int(altitude)
    except:
        observer.elevation = 0
    now = datetime.datetime.now()
    utc = datetime.datetime.utcnow()
    hour = now.hour
    observer.date = utc
    debug.debug('The local time is {:02}:{:02}:{:02} ({:02}:{:02}:{:02} UTC)'.format(now.hour,now.minute,now.second,
                                                                   utc.hour,utc.minute,utc.second))
    sun.compute(observer)
    current_sun_alt = sun.alt
    elevation = current_sun_alt*180/math.pi
    debug.debug('Elevation is: ',elevation,current_sun_alt)
    if elevation < twilightDegrees[twilight.lower()]:
        return 'night'
    if hour < 12:
        if elevation < 0:
            return 'morning'
        else:
            return 'daytime'
    elif hour >= 12:
        if elevation < 0:
            return 'evening'
    return 'daytime'

if __name__ == "__main__":
    debug.setdebug(1)
    print getTimeType(-123.9429,45.6134,42)
