import os
import sys
import json
import glob
from PIL import Image
from scipy import spatial
import numpy as np
import tile_31204

before_start_lets_do_some_calcuation = """
Source Lego set is 31204 Elvis Presley.
Contains 9 pc 16 x 16, which means width: 48, height: 48 (in Lego unit)

Every tile image is 30 x 30 pixels, so output image size will be 1440 x 1440 pixels

Notice: source image need to be squre
"""

def create_mosaic(main_photo_path: str, tiles_img_path: str):
    tile_size = (30, 30)
    outputHead, outputTail = os.path.splitext(main_photo_path)
    output_path = f"{outputHead}.legoize{outputTail}"

    # Get all tiles
    tile_paths = []
    for file in glob.glob(tiles_img_path):
        tile_paths.append(file)


    # Import and resize all tiles
    tiles = []
    for tile_path in tile_paths:
        tile = Image.open(tile_path)
        # tile = tile.resize(tile_size)     # Tile image should be 30 x 30 px
        tiles.append(tile)


    # Calculate dominant color
    colors = []
    for tile in tiles:
        mean_color = np.array(tile).mean(axis=0).mean(axis=0)
        colors.append(mean_color)


    # Pixelate (resize) main photo
    main_photo = Image.open(main_photo_path)

    width = int(np.round(main_photo.size[0] / tile_size[0]))
    height = int(np.round(main_photo.size[1] / tile_size[1]))

    resized_photo = main_photo.resize((width, height))

    # Find closest tile photo for every pixel
    tree = spatial.KDTree(colors)
    closest_tiles = np.zeros((width, height), dtype=np.uint32)

    for i in range(width):
        for j in range(height):
            closest = tree.query(resized_photo.getpixel((i, j)))
            closest_tiles[i, j] = closest[1]


    # Create an output image
    outputImg = Image.new('RGB', main_photo.size)

    # Count tiles
    tileCount = []
    for tile_path in tile_paths:
        tileDir, tileFileName = os.path.split(tile_path)
        tileName, tileExt = os.path.splitext(tileFileName)
        count = [tileName, 0]
        tileCount.append(count)

    # Draw tiles
    for i in range(width):
        for j in range(height):
            # Offset of tile
            x, y = i*tile_size[0], j*tile_size[1]
            # Index of tile
            index = closest_tiles[i, j]
            # Draw tile
            outputImg.paste(tiles[index], (x, y))
            # Count tile
            tileCount[index][1] += 1

    # Save output
    if os.path.exists(output_path):
        os.remove(output_path)
    outputImg.save(output_path)

    outputSummary(tileCount)

def outputSummary(tileCount):
    summary = {}
    for count in tileCount:
        summary[count[0]] = count[1]

    print(json.dumps(summary, indent=2))


main_photo_path = './image/test_1440-3.jpg'
create_mosaic(main_photo_path, tile_31204.tileColorPath)