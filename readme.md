# Purpose
This project started with a common question, where can I find a gift for my wife? <br/>
We love Lego, and I'm really impressed by Beatles and Elvis set. <br/><br/>
Here is an idea, whatif I can make a program which can input photo, output a instruction, then follow the instruction to build our own Lego mosaic picture. <br/>
Sounds amazing and fun! <br/><br/>
After so long, my wife got her gift. She is so happy to have it, the only one Lego mosaic in the world and totaly customized for her.<br/>
This project is not fully accomplished my all insane ideas, but I think pubish to public is not a bad idea.<br/>
Hope this project can help programmers having an alternative choice to make your unique own gift!<br/>


# Copyright declaration
This is a non profit, Lego fan oriented project. But I think copyright is always important and need to be clarified. <br/>
All images from Lego build instruction, whose copyright belongs to Lego company. <br/>


# User Manual: Genarate Build Instruction
1. Prepare source photo, image of tiles(default is 31204 Elvis). Images accept JPEG format.
2. Source photo should be squre size. (This project is inpired by Lego Beatles and Elvis, so I wanna generate a square Lego mosaic picture)
3. Source photo placed in `./image/sample.jpg` or you can change variable value in `main.py`
4. Run: `python main.py`
5. In folder `./image` will generate following files: <br\>
    * sample.lib-trad.jpg        Result of using template colors to transfer source photo.
    * sample.lib-trad-man.jpg    As Lego manual, repaint result with Lego instruction number.
    * sample.lib-trad-man.txt    Description of instruction number mapping to Lego tile's number. How many tiles will be using, tiles limit in the set, tile is enough or needs more.
    * sample.lib-trad-man-1.jpg  As Lego manual, similar to real Lego build instruction, split the whole `sample.lib-trad-man.jpg` to 9 parts. From 1 to 9 part of result with Lego instruction number.
    * ...
    * sample.lib-trad-man-9.jpg
6. `./tile_pool/31204_Elvis/LEGO-31204-color.png` can help you print your build instruction.
7. Enjoy building Lego!


# Programming Topic
## Python version
    3.9.13

## Setup Virtual environment
    python -m venv .venv

## Used packages
    Pillow, scipy, numpy
    pip install -r .\requirements.txt

## Reference
- [How to Create a Photo Mosaic in Python](https://towardsdatascience.com/how-to-create-a-photo-mosaic-in-python-45c94f6e8308)
- [BilHim @ github](https://gist.github.com/BilHim)

## 

# Lego
## Set
  - [Elvis](https://www.lego.com/en-us/service/buildinginstructions/31204)
  - [Beatles](https://www.lego.com/en-us/service/buildinginstructions/31198)

## About tiles knowledge
(In case I need to buy more tiles online)
- Square qube 1 x 1 x 1, 100 pc, weight 44 grams
- Square plate 1 x 1, 100 pc, weight 20 grams
- Squre tile 1 x 1, 100 pc, weight 16 grams
- Round tile 1 x 1, 100 pc, weight 11 grams [brickshop.eu](https://www.brickshop.eu/lego-parts/tiles/lego-tile-round-1x1-black-100-pcs.html)
