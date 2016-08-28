import colorsys


class Kolor:
    """represents color in rgb and hls representations
    accepts hex color code in __init__
    handles opacity (8 digit hex) by converting given color to a color as seen
    on a background
    """

    def __init__(self, hex, background='#FFFFFF'):
        """creates Kolor object from hex code
        :param hex: hex color code (6 or 8 digits)
        :param background: hex code of background color
        """
        self._hex = hex
        self._red, self._green, self._blue = [int(hex[1:3], 16)/255.,
                                              int(hex[3:5], 16)/255.,
                                              int(hex[5:7], 16)/255.]
        self._hue, self._luminance, self._saturation = colorsys.rgb_to_hls(
                                            self.red, self.green, self.blue)
        if len(hex) == 9:
            self._alpha = int(hex[-2:], 16)
            self._background = background
            self._convert_alpha_channel()

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        self._red = value
        self.update_hls()

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        self._green = value
        self.update_hls()

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        self._blue = value
        self.update_hls()

    @property
    def hue(self):
        return self._hue

    @hue.setter
    def hue(self, value):
        self._hue = value
        self.update_rgb()

    @property
    def saturation(self):
        return self._saturation

    @saturation.setter
    def saturation(self, value):
        self._saturation = value
        self.update_rgb()

    @property
    def luminance(self):
        return self._luminance

    @luminance.setter
    def luminance(self, value):
        self._luminance = value
        self.update_rgb()

    @property
    def hex(self):
        return "#{:02X}{:02X}{:02X}".format(round(self.red*255),
                                            round(self.green*255),
                                            round(self.blue*255))

    def update_rgb(self):
        self._red, self._green, self._blue = colorsys.hls_to_rgb(
            self.hue, self.luminance, self.saturation)

    def update_hls(self):
        self._hue, self._luminance, self._saturation = colorsys.rgb_to_hls(
                                            self.red, self.green, self.blue)

    def _convert_alpha_channel(self):
        """changes base color (first 6 hex digits) to a color on background
        with opacity (last 2 hex digits)
        """
        a = self._alpha/255.
        bg = Kolor(self._background)
        self.luminance = (1. - a) * bg.luminance + a * self.luminance
