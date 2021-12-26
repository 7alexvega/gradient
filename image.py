import io
import os

import numpy as np
import scipy
import scipy.cluster
import scipy.misc
from PIL import Image as Pillow, ImageFilter

from config import config
from windows import Windows


class Image:
    def __init__(self):
        self.windows = Windows()
        os.makedirs(config["image"]["wallpaper_dir"], exist_ok=True)

    def get_dominant_colors(self, image_path, n):
        image = Pillow.open(image_path).resize((150, 150))

        array = np.asarray(image)
        shape = array.shape
        array = array.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

        codes, dist = scipy.cluster.vq.kmeans(array, n)

        dominant_colors = []
        for i in range(n):
            rgb = (int(codes[i][0]), int(codes[i][1]), int(codes[i][2]))
            dominant_colors.append(rgb)

        return dominant_colors

    def create_wallpaper(self, album_art, name):
        extension = config["image"]["extension"]
        name = f'{name}.{extension}' if extension not in name else name
        background_save_path = os.path.abspath(os.path.join(config["image"]["wallpaper_dir"], name))

        album_art_image = Pillow.open(io.BytesIO(album_art))

        screen_size = self.windows.get_screen_size()
        height = screen_size['height']
        width = screen_size['width']

        major_axis_length = max(height, width)

        background = album_art_image.resize((major_axis_length, major_axis_length))
        background = background.filter(ImageFilter.GaussianBlur(radius=config["image"]["background_blur_amount"]))

        upper = 0
        left = (major_axis_length - height) // 2
        right = width
        lower = (major_axis_length + height) // 2

        background = background.crop((upper, left, right, lower))

        aligned_center_of_screen = ((int((background.size[0] / 2) - (album_art_image.size[0] / 2))),
                                    (int((background.size[1] / 2) - (album_art_image.size[1] / 2))))

        background.paste(album_art_image, aligned_center_of_screen)

        background.save(background_save_path)
        return background_save_path
