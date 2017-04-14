""" Simple example of reading an image in as greyscale """
from skimage import io

FILEPATH = './Practice Data/0.jpg'
IMG_ARRAY = io.imread(FILEPATH, as_grey=True)

print(IMG_ARRAY[0])
