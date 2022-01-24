import atexit
import json
import os
import time

from config import config
from hue import Hue
from image import Image
from spotify import Spotify
from windows import Windows


class Gradient:

    def __init__(self):
        self.cache = self.get_cache()

    def get_cache(self):
        if os.path.exists('db.json'):
            with open('db.json', 'r') as file:
                cache = json.load(file)
        else:
            cache = dict()
        return cache

    def start(self):
        spotify = Spotify()
        windows = Windows()
        image = Image()
        hue = Hue()

        atexit.register(windows.revert_wallpaper)
        atexit.register(lambda: json.dump(self.cache, open('db.json', 'w')))

        previous_song = None

        while True:
            current_song = windows.get_current_song()

            if current_song:

                song_changed = current_song != previous_song
                if song_changed:
                    previous_song = current_song

                    album_art_url = spotify.get_current_album_art_url()
                    album_key = album_art_url.rsplit('/')[-1]

                    if album_key in self.cache and os.path.exists(self.cache[album_key]):
                        wallpaper_path = self.cache[album_key]
                    else:
                        album_art = spotify.get_album_art_image(album_art_url)
                        wallpaper_path = image.create_wallpaper(album_art, album_key)
                        self.cache[album_key] = wallpaper_path

                    hue_lights = config['hue']['lights']

                    dominant_colors = image.get_dominant_colors(wallpaper_path, len(hue_lights))
                    for i in range(len(dominant_colors)):
                        light = hue_lights[i]
                        color = dominant_colors[i]
                        hue.update_light_color(light, color)
                    windows.set_wallpaper(wallpaper_path)

            else:
                windows.revert_wallpaper()

            time.sleep(config['gradient']['refresh_delay_s'])


if __name__ == '__main__':
    gradient = Gradient()
    gradient.start()
