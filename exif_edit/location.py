"""
This module contains functionality related to geo location.
"""
from exif_edit.formats import DegreeFormatFactory, Format

class Coordinate:
    """
    Represent a coordinate on the globe.
    """
    def __init__(self, latitude, longitude, lat_ref = 'N', lon_ref = 'E'):
        if not isinstance(latitude, Format):
            latitude = DegreeFormatFactory.create(latitude)
        self.latitude = latitude
        self.lat_ref = lat_ref

        if not isinstance(longitude, Format):
            longitude = DegreeFormatFactory.create(longitude)
        self.longitude = longitude
        self.lon_ref = lon_ref

    def decimal(self):
        lat_dec = abs(self.latitude.as_float())
        lon_dec = abs(self.longitude.as_float())
        lat = lat_dec if self.lat_ref == 'N' else -1 * lat_dec
        lon = lon_dec if self.lon_ref == 'E' else -1 * lon_dec
        return lat, lon

    def google_maps_url(self):
        lat, lon = self.decimal()
        return f"https://www.google.com/maps/place/{lat}+{lon}/@{lat},{lon},10z"