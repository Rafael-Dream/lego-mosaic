import os
from PIL import Image

ROOT_DIR = None
TILE_SIZE = (30, 30)
GRID_DIMS = (48, 48)


def getOutputPath(input_path, postfix='legoize', fileExt=None):
  outputHead, outputTail = os.path.splitext(input_path)
  if None != fileExt:
    outputTail = fileExt
  return f"{outputHead}.{postfix}{outputTail}"
