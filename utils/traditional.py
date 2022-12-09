import os
import sys
import json
import glob
from PIL import Image
from scipy import spatial
import numpy as np
from . import common
from . import genEditor

## Reference site:
# https://towardsdatascience.com/how-to-create-a-photo-mosaic-in-python-45c94f6e8308
## Requirements:
# Pillow
# scipy
# numpy

def create_mosaic(main_photo_path: str, tiles_img_path: str, tile_limit):

    # Get all tiles
    tile_paths = []
    for file in glob.glob(tiles_img_path):
        tile_paths.append(file)


    # Init
    tiles = []
    limits = []
    manual_tiles = []
    tileCount = []
    for tile_path in tile_paths:
        # Import and resize all tiles
        tile = Image.open(tile_path)
        # tile = tile.resize(common.TILE_SIZE)     # Tile image should be 30 x 30 px, skip this step
        tiles.append(tile)
        # Import manual tiles
        manual_tile_path = tile_path.replace("color", "manual")
        manual_tile = Image.open(manual_tile_path)
        manual_tiles.append(manual_tile)
        # Init counting array
        tileName = os.path.splitext(os.path.basename(tile_path))[0]
        if tileName in tile_limit:
            limits.append([tileName, tile_limit[tileName]])
        else:
            limits.append([tileName, 0])
        tileCount.append([tileName, 0])

    # Calculate dominant color
    colors = []
    for tile in tiles:
        mean_color = np.array(tile).mean(axis=0).mean(axis=0)
        colors.append(mean_color)

#---------------------------
# TODO: Change this section.
# 1. Consider highlight
#---------------------------
    # Pixelate (resize) main photo
    main_photo = Image.open(main_photo_path)
    width = int(np.round(main_photo.size[0] / common.TILE_SIZE[0]))
    height = int(np.round(main_photo.size[1] / common.TILE_SIZE[1]))
    resized_photo = main_photo.resize((width, height))

    # Find closest tile photo for every pixel, and consider brick limit
    tree = spatial.KDTree(colors)
    closest_tiles = np.zeros((width, height), dtype=np.uint32)
    for i in range(width):
        for j in range(height):
            closest = tree.query(resized_photo.getpixel((i, j)), k=10)

            found = False
            for idxTry in range(10):
                index = closest[1][idxTry]
                curCount = tileCount[index][1]
                if ((limits[index][1] - curCount) > 0) or (limits[index][1] == 0):
                    closest_tiles[i, j] = index
                    tileCount[index][1] += 1
                    found = True
                    break

            if not found:
                index = closest[1][0]
                closest_tiles[i, j] = index
                tileCount[index][1] += 1
#---------------------------


    # Create output images
    outputImg = Image.new('RGB', main_photo.size)
    outputManualImg = Image.new('RGB', main_photo.size)
    outputManualPartImgs = []

    # Draw tiles
    for i in range(width):
        for j in range(height):
            # Offset of tile
            x, y = i*common.TILE_SIZE[0], j*common.TILE_SIZE[1]
            # Index of tile
            index = closest_tiles[i, j]
            # Draw tile
            outputImg.paste(tiles[index], (x, y))
            outputManualImg.paste(manual_tiles[index], (x, y))
            # Count tile
            #tileCount[index][1] += 1

    # Draw manual part tiles
    # 0-0 0,0 ~ 5,5
    # 0-1 6,0 ~ 11,5
    # 0-2 12,0 ~ 17,5
    # 0-0 0-1 0-2
    # 1-0 1-1 1-2
    # 2-0 2-1 2-2
    widthPart = int(width / 3)
    heightPart = int(height / 3)
    MANUAL_PART_SIZE = (widthPart*common.TILE_SIZE[0], heightPart*common.TILE_SIZE[1])
    for mj in range(3):
        for mi in range(3):
            outputManualPartImg = Image.new('RGB', MANUAL_PART_SIZE)
            for i in range(widthPart):
                for j in range(heightPart):
                    # Offset of tile
                    x, y = i*common.TILE_SIZE[0], j*common.TILE_SIZE[1]
                    # Index of tile
                    real_i = i + (mi * widthPart)
                    real_j = j + (mj * heightPart)
                    index = closest_tiles[real_i, real_j]
                    # Draw tile
                    outputManualPartImg.paste(manual_tiles[index], (x, y))
            outputManualPartImgs.append([(mj*3 + mi + 1), outputManualPartImg])


    ## Save output
    # After legoize, full Image
    output_path = common.getOutputPath(main_photo_path, "lib-trad")
    outputImgToFile(outputImg, output_path)
    # Legoize manual: full size
    outputManual_path = common.getOutputPath(main_photo_path, "lib-trad-man")
    outputImgToFile(outputManualImg, outputManual_path)
    # Legoize manual: slice to nine pieces of image
    for outputManualPart in outputManualPartImgs:
        outputImgToFile(outputManualPart[1], common.getOutputPath(main_photo_path, f"lib-trad-man-{outputManualPart[0]}"))
    # Text summary
    txtPath = common.getOutputPath(main_photo_path, "lib-trad-man", ".txt")
    outputSummary(tileCount, tile_limit, txtPath)
    
    # Generate html editor for further fine tune
    genEditor.run(output_path, tiles_img_path, tile_limit)




def outputImgToFile(outputImg, output_path):
    if os.path.exists(output_path):
        os.remove(output_path)
    outputImg.save(output_path)


def outputSummary(tileCount, tileLimit, txtPath):
    summary = {}
    for count in tileCount:
        name = count[0]
        using = count[1]
        limit = tileLimit[name]
        rest = limit - using
        tmp = f"using: {str(using).ljust(6)}| limit: {str(limit).ljust(6)}"
        if rest > 0:
            tmp += f"| unuse: {rest}"
        elif rest < 0:
            tmp += f"| need more: {rest}"
        else:
            tmp += f"| ok"
        summary[name] = tmp

    txtContent = json.dumps(summary, indent=2)
    print(txtContent)

    if os.path.exists(txtPath):
        os.remove(txtPath)
    f = open(txtPath, "w")
    f.write(txtContent)
    f.close()
