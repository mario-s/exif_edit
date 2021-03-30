from enum import Enum
import logging

import exif as ex

from exif_edit.geoloc import Factory

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
    def cast(cls, key, value):
        """Converts a string value to a proper type."""
        #do we have a matching enum in our dictionary?
        if key in cls.dictionary:
            return cls.__from_enum(key, value)
        try:
            return int(value)
        except:
            return value

    @staticmethod
    def try_read(dic, key):
        """
        This method tries to get the value from the dictionary, and if it is an enum, 
        return the name of it.
        """
        try:
            #this may fail if there is an illegal value for the key
            value = dic.get(key)
            if Converter.__is_geoloc(key):
                return Factory.create(value)
            #human readable value if we have an enum
            if isinstance(value, Enum):
                return value.name
            return value
        except ValueError as exc:
            logging.warning("Illegal value in exif: %s", exc)
            return None

    @staticmethod 
    def __is_geoloc(key):
        return key in ("gps_longitude", "gps_latitude")

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