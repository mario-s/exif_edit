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
