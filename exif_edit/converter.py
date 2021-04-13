"""
Module for converting between UI and Exif data.
"""
from enum import Enum
import logging

from sortedcontainers import SortedDict
import exif as ex

from exif_edit.formats import DegreeFormatFactory, Format, TimeStamp


class ExifFilter:
    """Filter for keys which should be handled different."""

    @staticmethod
    def locked():
        """This method joins all filter into one."""
        return ExifFilter.not_deleteable() + ExifFilter.read_only()

    @staticmethod
    def not_deleteable():
        """Filter for attributes which are editable bot not deletable."""
        return ("bits_per_sample", "compression",
            "image_height", "image_width", "image_unique_id",
            "jpeg_interchange_format", "jpeg_interchange_format_length",
            "photometric_interpretation",
            "resolution_unit",
            "samples_per_pixel", "x_resolution", "y_resolution")

    @staticmethod
    def read_only():
        """Filter for attributes which are read only."""
        return "_exif_ifd_pointer", "exif_version"


class Converter:
    """This class acts as a converter between the exif data and the data from the sheet."""

    dictionary = {"color_space": ex.ColorSpace,
            "exposure_mode": ex.ExposureMode,
            "exposure_program": ex.ExposureProgram,
            "gps_altitude_ref": ex.GpsAltitudeRef,
            "light_source": ex.LightSource,
            "metering_mode": ex.MeteringMode,
            "orientation": ex.Orientation,
            "resolution_unit": ex.ResolutionUnit,
            "saturation": ex.Saturation,
            "scene_capture_type": ex.SceneCaptureType,
            "sensing_method": ex.SensingMethod,
            "sharpness": ex.Sharpness,
            "white_balance": ex.WhiteBalance}

    @classmethod
    def keys(cls) -> list:
        """Returns a list of keys from the dictionary."""
        return list(cls.dictionary.keys())

    @classmethod
    def __from_enum(cls, key, value):
        enm = cls.dictionary[key]
        try:
            return enm(int(value))
        except:
            #is the value a valid enum name?
            if value in enm.__members__:
                return enm[value]
            #fallback to first enum value
            return list(enm)[0]

    @classmethod
    def to_exif(cls, key, value):
        """Converts the value from the sheet to a exif conform type."""
        #do we have a matching enum in our dictionary?
        if key in cls.dictionary:
            return cls.__from_enum(key, value)
        #do we have a custom type?
        if isinstance(value, Format):
            return value.get_source()
        try:
            return int(value)
        except:
            return value

    @staticmethod
    def read_from_dict(dic, key):
        """
        This method tries to get the value from the dictionary, and if it is an enum,
        return the name of it.
        """
        try:
            #this may fail if there is an illegal value for the key
            value = dic.get(key)
            return Converter.to_format(key, value)
        except ValueError as exc:
            logging.warning("Illegal value in exif: %s", exc)
            return None

    @staticmethod
    def to_format(key, value):
        """
        Converts value to existing custom formats.
        """
        if Converter.is_gps_timestamp(key):
                return TimeStamp.parse(value)
        if Converter.is_geoloc(key):
            return DegreeFormatFactory.create(value)
        #human readable value if we have an enum
        if isinstance(value, Enum):
            return value.name
        return value

    @staticmethod
    def is_geoloc(key) -> bool:
        """
        This function returns True if the key is related to a geo location, else False"
        """
        return key in ("gps_longitude", "gps_latitude")

    @staticmethod
    def is_gps_timestamp(key) -> bool:
        """
        This function returns True if the key is related to a gps timestamp, else False"
        """
        return key in ("gps_timestamp", )

    @staticmethod
    def rows_to_dict(rows) -> dict:
        """
        This method converts a collection of rows into a dictionary.
        """
        dic = {}
        for col in rows:
            if len(col) < 2:
                raise ValueError("Expect at least two cells in the row")
            dic[col[0]] = col[1]
        return dic

    @staticmethod
    def group_dict(dic) -> dict:
        """
        Groups the given dictionary, where every group is sorted.
        """
        #sort elements seperately, which can only be read
        read_only = SortedDict(Converter.__filter(dic, ExifFilter.read_only()))
        #sort elements seperately, which can not be deleted
        edit_only = SortedDict(Converter.__filter(dic, ExifFilter.not_deleteable()))
        #join the dictionaries
        return read_only | edit_only | SortedDict(dic)

    @staticmethod
    def __filter(dic, fltr):
        """
        Remove elements from dictionary to avoid sorting them in the big one.
        """
        return [(k, dic.pop(k)) for k in fltr if k in dic]
