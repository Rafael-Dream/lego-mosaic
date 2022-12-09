# reference site:
# danielballan/photomosaic
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from . import common
from skimage import data, img_as_float
from skimage.io import imread, imsave
import photomosaic as pm


def create_mosaic(main_photo_path: str, tiles_img_path: str):

    grid_dims = common.GRID_DIMS
    depth = 0

    # To begin, you need an image that you want to mosaic-ify. You can load it like so:
    image = imread(main_photo_path)
    # image = data.chelsea()  # cat picture!

    # Next, you need large collection of images to fill in the tiles in the mosaic.
    # If you don’t have a large collection of images handy, you can generate a collection of solid-color squares.
    # Real photos are more interesting, but solid-color squares are nice for experimentation.
    # Generate a collection of solid-color square images.
    # pm.rainbow_of_squares('pool/')
    # Analyze the collection (the "pool") of images.
    # pool = pm.make_pool('pool/*.png')
    pool = pm.make_pool(tiles_img_path)

    # Create a mosiac.
    # Basic:
    # To make a more detailed mosaic, subdivide tiles in important regions.
    # The optional depth parameter selectively splits tiles into quadrants if they contain a certain amount of contrast.
    # mos = pm.basic_mosaic(image, pool, grid_dims, depth=depth)

    # Size the image to be evenly divisible by the tiles.
    image = img_as_float(image)
    image = pm.rescale_commensurate(image, grid_dims, depth)

    # Use perceptually uniform colorspace for all analysis.
    converted_img = pm.perceptual(image)

    # Adapt the color palette of the image to resemble the palette of the pool.
    adapted_img = pm.adapt_to_pool(converted_img, pool)

    # Partition the image into tiles and characterize each one's color.
    tiles = pm.partition(adapted_img, grid_dims=grid_dims,
                         mask=None, depth=depth)
    tile_colors = [np.mean(adapted_img[tile].reshape(-1, 3), 0)
                   for tile in tqdm(tiles, desc='analyzing tiles')]

    # Match a pool image to each tile.
    match = pm.simple_matcher(pool)
    matches = [match(tc) for tc in tqdm(tile_colors, desc='matching')]

    # Draw the mosaic.
    canvas = np.ones_like(image)  # white canvas same shape as input image
    mos = pm.draw_mosaic(canvas, tiles, matches)

    # Now mos is our mosaic. We can save it
    saveMosToFile(mos, common.getOutputPath(main_photo_path, f"lib-phomo-{depth}"))

    ## Experiment.
    ## Not fit legoize spec. depth cause result tile not in the same size.
    # depth = 1
    # saveMosToFile(pm.basic_mosaic(image, pool, grid_dims=grid_dims, depth=depth), common.getOutputPath(main_photo_path, f"lib-phomo-{depth}"))
    # depth = 5
    #saveMosToFile(pm.basic_mosaic(image, pool, grid_dims=grid_dims, depth=depth), common.getOutputPath(main_photo_path, f"lib-phomo-{depth}"))

    # or plot it using matplotlib.
    # plt.imshow(mos)
    # input("Press Enter to finish ...")


def saveMosToFile(mos, output_path):
    if os.path.exists(output_path):
        os.remove(output_path)
    imsave(output_path, mos)
