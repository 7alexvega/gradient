import numpy as np
import scipy
import scipy.cluster
import scipy.misc
from PIL import Image as Pillow


class Image:

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
