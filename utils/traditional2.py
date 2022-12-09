## Reference site:
# https://medium.com/@aarongrove/creating-image-mosaics-with-python-8e4c25dd9bf9
import os
import glob
import random
from PIL import Image
import numpy as np
from scipy import spatial
from . import common


def create_mosaic(main_photo_path: str, tiles_img_path: str):
  grid_dim = common.GRID_DIMS
  output_path = common.getOutputPath(main_photo_path, "trad2")

  ## 1. Firstly, the image we would like to recreate is loaded and the np.asarray() function is used to store the image as a numpy array.
  face_im_arr = load_image(main_photo_path)

  ## 2. Now we must make the template for our final image. To do this, we pixelate the image we would like to recreate by slicing our numpy array, calling for every nth pixel for each row and column.
  mos_template = face_im_arr[::10,::10]

  ## 3. Next, we must load all of the images that we want to use as mosaic tiles. These are stored in three-dimensional numpy arrays just like the template image. Each of these 3-d arrays are stored in one four-dimensional array. Now that we have all of the images, they can be assessed against the pixels of the template image.
  images = []
  for file in glob.glob(tiles_img_path):
    im = load_image(file)
    images.append(im)
  # The images then go through resizing
  images_array = np.asarray(images)

  ## 4. Now it gets interesting… We need to access each pixel of the template image, read its colour values (RGB) then find the closest representation of this colour within the image set. The idea being that the chosen image will be the one to replace that pixel in the final image.
  ## To do this we need a single RGB value for each of the mosaic images, so in a separate array the mean RGB values are stored.
  image_values = np.apply_over_axes(np.mean, images_array, [1,2]).reshape(len(images),3)
  ## The block above will get the mean R, G and B values for each image and store it in a new 3D array.
  ## Now there is an array of mean RGB values representing each of our mosaic images that we can directly compare to each pixel in the template image. To do this we use a ‘KDTree’, a binary tree that will hold a data point for each of the RGB values in our image_values array.

  ## We initialise the KDTree by passing our image_values array to it. Now the tree can be queried with a set of RGB values and it will find the closest match in image_values.
  tree = spatial.KDTree(image_values)

  ## So all that is left to do is iterate through every pixel in the template image, pass the tree its RGB values and store the index of the closest image from our mosaic image mean RGB values.
  image_idx = np.zeros(grid_dim, dtype=np.uint32)
  for i in range(grid_dim[0]):
    for j in range(grid_dim[1]):
      template = mos_template[i, j]
      match = tree.query(template, k=40)
      pick = random.randint(0, 39)
      image_idx[i, j] = match[1][pick]

  ## 5. Now we must build the final image. We can pass the indices stored from finding the nearest RGB values of each template pixel to our array which holds all of our full mosaic images. These images can then be pasted onto a canvas, offsetting the position so that each image is placed where the template pixel it corresponds to would sit.
  canvas = Image.new('RGB', (common.TILE_SIZE[0]*grid_dim[0], common.TILE_SIZE[1]*grid_dim[1]))
  for i in range(grid_dim[0]):
    for j in range(grid_dim[1]):
      arr = images[image_idx[i, j]]
      x, y = i*common.TILE_SIZE[0], j*common.TILE_SIZE[1]
      im = Image.fromarray(arr)
      canvas.paste(im, (x,y))

  # Save output
  if os.path.exists(output_path):
      os.remove(output_path)
  canvas.save(output_path)

def load_image(source : str) -> np.ndarray:
  '''
  Opens an image from specified source and returns a numpy array
  with image rgb data
  '''
  with Image.open(source) as im:
      im_arr = np.asarray(im)
  return im_arr