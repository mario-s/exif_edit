from enum import Enum
import exif as ex
import re

class Converter:

    """This class converts between the human readable values and the Enum values."""

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
            "sending_method": ex.SensingMethod,
            "sharpness": ex.Sharpness,
            "white_balance": ex.WhiteBalance}

    pattern = re.compile('\d')

    @classmethod
    def keys(cls):
        return list(cls.dictionary.keys())

    @classmethod
    def __from_enum(cls, key, value):
        en = cls.dictionary[key]
        #is it a number?
        if cls.pattern.match(value):
            try:
                return en(int(value))
            except:
                return list(en)[0]
        #is the value a valid enum name?
        elif value in en.__members__:
            return en[value]
        #fallback to first enum value
        return list(en)[0]

    """Converts a string value to a proper type."""
    @classmethod
    def cast(cls, key, value):
        #do we have a matching enum in our dictionary?
        if key in cls.dictionary:
            return cls.__from_enum(key, value)
        else:
            try:
                return int(value)
            except:
                return value


        
