"""
This module contains functionality related to geo location.
"""
from typing import Tuple
from exif_edit.formats import DegreeFormatFactory, DegreeFormat

class Coordinate:
    """
    Represent a coordinate on the globe.
    """
    def __init__(self, latitude, longitude, lat_ref = 'N', lon_ref = 'E'):
        #convert to an appropriate format
        if not isinstance(latitude, DegreeFormat):
            latitude = DegreeFormatFactory.create(latitude)
        self.latitude = latitude
        if not isinstance(longitude, DegreeFormat):
            longitude = DegreeFormatFactory.create(longitude)
        self.longitude = longitude

        self.lat_ref = lat_ref
        self.lon_ref = lon_ref

    def decimal(self) -> Tuple:
        """
        This retuns the coordinate in decimal format.
        """
        lat_dec = abs(self.latitude.as_float())
        lon_dec = abs(self.longitude.as_float())
        lat = lat_dec if self.lat_ref == 'N' else -1 * lat_dec
        lon = lon_dec if self.lon_ref == 'E' else -1 * lon_dec
        return lat, lon

    def google_maps_url(self):
        """
        This returns the URL to Google's Maps.
        """
        lat, lon = self.decimal()
        return f"https://www.google.com/maps/place/{lat}+{lon}/@{lat},{lon},10z"
