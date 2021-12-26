import math

import requests

from config import config


class Hue:
    def rgb_to_xy(self, rgb):

        red = rgb[0] / 255
        green = rgb[1] / 255
        blue = rgb[2] / 255

        red = ((red + 0.055) / (1.0 + 0.055)) ** 2.4 if red > 0.04045 else (red / 12.92)
        green = ((green + 0.055) / (1.0 + 0.055)) ** 2.4 if green > 0.04045 else (green / 12.92)
        blue = ((blue + 0.055) / (1.0 + 0.055)) ** 2.4 if blue > 0.04045 else (blue / 12.92)

        x = red * 0.664511 + green * 0.154324 + blue * 0.162028
        y = red * 0.283881 + green * 0.668433 + blue * 0.047685
        z = red * 0.000088 + green * 0.072310 + blue * 0.986039

        fx = x / (x + y + z)
        fy = y / (x + y + z)

        if math.isnan(fx):
            fx = 0.0
        if math.isnan(fy):
            fy = 0.0

        return '[' + f'{fx:.4f}' + ',' + f'{fy:.4f}' + ']'

    def update_light_color(self, light, rgb):
        color = self.rgb_to_xy(rgb)
        bridge_config = config["hue"]["bridge"]
        url = f'{bridge_config["scheme"]}://{bridge_config["host"]}/api/{bridge_config["api_key"]}/lights/{light}/state/'
        data = '{"xy": ' + color + ', "bri":254, "sat":254}'
        requests.put(url, data)
