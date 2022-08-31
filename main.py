import sys
import glob
from PIL import Image
from scipy import spatial
import numpy as np

main_photo_path = './img_src/20220120.jpg'
tile_photos_path = './tile_pool/31198_Beatles'
tile_size = (int(sys.argv[3]), int(sys.argv[4]))
output_path = sys.argv[5]

# Get all tiles
tile_paths = []
for file in glob.glob(tile_photos_path):
    tile_paths.append(file)


# Import and resize all tiles
tiles = []
for path in tile_paths:
    tile = Image.open(path)
    tile = tile.resize(tile_size)
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
output = Image.new('RGB', main_photo.size)

# Draw tiles
for i in range(width):
    for j in range(height):
        # Offset of tile
        x, y = i*tile_size[0], j*tile_size[1]
        # Index of tile
        index = closest_tiles[i, j]
        # Draw tile
        output.paste(tiles[index], (x, y))

# Save output
output.save(output_path)