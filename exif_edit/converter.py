from enum import Enum
import exif as ex

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

    @classmethod
    def keys(cls):
        return list(cls.dictionary.keys())

    """Converts a string value to a proper type."""
    @classmethod
    def cast(cls, key, value):
        #do we have a matching enum in our dictionary?
        if key in cls.dictionary:
            en = cls.dictionary[key]
            #is the value a valid enum name?
            if value in en.__members__:
                return en[value]
            #fallback to first enum value
            return list(en)[0]
        else:
            try:
                return int(value)
            except:
                return value
        
