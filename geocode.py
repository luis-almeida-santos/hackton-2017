import json
import sys

from diskcache import FanoutCache
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim
import logging

geocoders = [
    Nominatim(),
    GoogleV3()
]

location_cache = FanoutCache('./geo-location-cache', shards=4, timeout=1)

def geocode_location(location_string):

    #logging.debug("Looking for: %s; Cached: %s" % (location_string, location_string in location_cache))

    location = None

    if location_string in location_cache:
        return location_cache[location_string]
    else:
        for geolocator in geocoders:
            if location is None:
                location = geolocator.geocode(location_string)
            else:
                break

    if location is None:
        print "%d NOT found in any geo location service" % location_string
    else:
        logging.debug("%s =>  address: %s --> lat/long: %f - %f " % (location_string, location.address, location.latitude, location.longitude))
        location_cache[location_string] = location

    return location

def close():
    location_cache.close()