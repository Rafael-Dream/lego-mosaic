import os
import glob
from pathlib import Path
from PIL import Image
import numpy as np
from scipy import spatial
from . import common
from legoObj.tile import Tile


def run(legoize_img_path: str, tiles_img_path: str, tile_limit):

  # Init all tiles info
  tiles = []
  for tile_path in glob.glob(tiles_img_path):
    tileName = os.path.splitext(os.path.basename(tile_path))[0]
    img = Image.open(tile_path)
    tile = Tile(tileName, tile_path, tile_path.replace("color", "manual"))
    tile.hexColor = readTileToHexColor(img)
    tile.limitCount = 0 if not tileName in tile_limit else tile_limit[tileName]
    tile.meanColor = np.array(img).mean(axis=0).mean(axis=0)
    tiles.append(tile)

  tree = spatial.KDTree(extractAttrList(tiles, "meanColor"))

  legoizeImg = Image.open(legoize_img_path)
  stepX = int(np.round(legoizeImg.size[0] / common.TILE_SIZE[0]))
  stepY = int(np.round(legoizeImg.size[1] / common.TILE_SIZE[1]))

  # Mapping legoize image to tile
  legoizeIdxs = np.zeros((stepX, stepY), dtype=np.uint32)
  for i in range(stepX):
    for j in range(stepY):
      closest = tree.query(legoizeImg.getpixel(((i*common.TILE_SIZE[0])+5, (j*common.TILE_SIZE[1])+5)))
      idx = closest[1]
      legoizeIdxs[i, j] = idx
      tiles[idx].usedCount += 1

  # Generate js for html editor
  outputHtmlPath = common.getOutputPath(legoize_img_path, "editor", ".html")
  outputJsPath = common.getOutputPath(legoize_img_path, "editor", ".js")
  imgName = os.path.splitext(os.path.basename(legoize_img_path))[0]
  genEditorHtml(outputHtmlPath, outputJsPath)
  genEditorJs(outputJsPath, imgName, tiles, legoizeIdxs, stepX, stepY)


def readTileToHexColor(img) -> str:
  # Assume tile image has the same color in whole image
  pixels = img.load()
  width, height = img.size
  cx = int(width / 2)
  cy = int(height / 2)
  r, g, b = pixels[cx, cy]
  return f"#{r:02x}{g:02x}{b:02x}"


def extractAttrList(tiles: list, attrName: str) -> list:
  result = []
  for tile in tiles:
    result.append(getattr(tile, attrName))
  return result


def genEditorHtml(outputHtmlPath: str, outputJsPath: str):
  tmplate = Path(os.path.join(common.ROOT_DIR, 'htmlEditor/index.html')).read_text()

  content = tmplate.replace('"sample.js"', f'"{os.path.basename(outputJsPath)}"')

  with open(outputHtmlPath, "w") as outputFile:
    outputFile.write(content)


def genEditorJs(outputJsPath: str, title: str, srcTiles, legoizeIdxs, stepX, stepY):
  tmplate = Path(os.path.join(common.ROOT_DIR, 'htmlEditor/template.js')).read_text()

  tilesData = []
  for tile in srcTiles:
    tilesData.append(tile.genHtmlJson())

  imgRows = []
  for j in range(stepY):
    imgRow = []
    for i in range(stepX):
      imgRow.append(str(legoizeIdxs[i, j]))
    imgRows.append(f"  [{','.join(imgRow)}]")


  content = tmplate.replace('__PAGE_TITLE__', title).replace('__TILES_DATA__', ',\n'.join(tilesData)).replace('__IMG_TILES_DATA__', ',\n'.join(imgRows))

  with open(outputJsPath, "w") as outputFile:
    outputFile.write(content)
