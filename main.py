import os
import sys
from utils import common
from utils import traditional
from utils import traditional2
from utils import photomosaic
import tile_31204


common.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

before_start_lets_do_some_calcuation = """
Source Lego set is 31204 Elvis Presley.
Contains 9 pc 16 x 16, which means width: 48, height: 48 (in Lego unit)

Every tile image is 30 x 30 pixels, so output image size will be 1440 x 1440 pixels

Notice: source image need to be squre
"""


main_photo_path = './image/test-mayday/test_1440-3.jpg'
main_photo_path = './image/test2/B-1440.jpg'

traditional.create_mosaic(os.path.join(common.ROOT_DIR, main_photo_path), os.path.join(common.ROOT_DIR, tile_31204.tileColorPath), tile_31204.tileCount)
# traditional2.create_mosaic(os.path.join(common.ROOT_DIR, main_photo_path), os.path.join(common.ROOT_DIR, tile_31204.tileColorPath))
# photomosaic.create_mosaic(os.path.join(common.ROOT_DIR, main_photo_path), os.path.join(common.ROOT_DIR, tile_31204.tileColorPath))


