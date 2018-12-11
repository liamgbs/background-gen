from PIL import Image, ImageDraw
from random import randint, choice
from FortunesAlgorithm import Fortunes
from FractalTree import FractalTree
from helpers import randomColour
from colours import Colours, brightness
import sys

imgx = 4096
imgy = 2160

tilt_lower = 70
tilt_higher = 110

background_alpha = 120

bright_threshold = 130

def get_args():
    do_tree, do_tess = False, False

    if len(sys.argv) == 1:
        do_tree, do_tess = True, True
    else:
        argslower = [arg.lower() for arg in sys.argv]
        print(argslower)
        if "tree" in argslower: do_tree = True
        if "tess" in argslower: do_tess = True
    return do_tree, do_tess

def main():
    do_tree, do_tess = get_args()

    c = Colours(background_alpha).complimentary()

    image = Image.new("RGBA", (imgx, imgy), choice(c))
    draw = ImageDraw.Draw(image)

    if do_tess:
        f = Fortunes(imgx, imgy)
        for p in f.get_polygons():
            draw.polygon(list(p.exterior.coords), fill=choice(c))

    if do_tree:
        bright = True if brightness(c) > bright_threshold else False
        rbg_low, rbg_high = (bright_threshold, 255) if bright else (0, bright_threshold)

        FractalTree(imgx, imgy, draw).draw(imgx / 2,
                                          imgy,
                                          randint(-tilt_higher, -tilt_lower),
                                          branches=10,
                                          branch_width=20,
                                          colour=randomColour(rbg_low, rbg_high),
                                          bright=brightness(c) > bright_threshold)

    image.save("background.png", "PNG")


if __name__ == '__main__':
  main()
