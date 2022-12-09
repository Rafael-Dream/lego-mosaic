class Tile:
  # Tile name
  name = None

  # Image path: file path, tile image, assume is pure color image
  imgPath = None

  # Manual image path: file path, synchronize to tile image, for output construction manual
  manImgPath = None

  # Mean color
  meanColor = None

  # Image's color in hex format, for output html
  hexColor = None

  # Tile's count number in Lego set
  limitCount = 0

  # Used tile count
  usedCount = 0

  def __init__(self, name: str, imgPath: str, manImgPath: str):
    self.name = name
    self.imgPath = imgPath
    self.manImgPath = manImgPath
    self.limitCount = 0
    self.usedCount = 0


  def genHtmlJson(self) -> str:
    return f'{{"name":"{self.name}", "color":"{self.hexColor}", "limit":"{self.limitCount}", "used":"{self.usedCount}"}}'