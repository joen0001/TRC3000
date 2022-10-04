from PIL import Image, ImageDraw, ImageFont
import numpy as np

def foam(image_path, GRID_BOX_SIZE=50, THRESHOLD = 50):
    im = Image.open(image_path) # Can be many different formats.
    width,height = im.size  # Get the width and hight of the image for iterating over

    area = (width/2-GRID_BOX_SIZE/2,0,width/2+GRID_BOX_SIZE/2,height)
    crop = im.crop(area)

    draw = ImageDraw.Draw(im)
    #draw.rectangle(area, outline=(R,G,B), width=10)

    width_crop,height_crop = crop.size
    n = width_crop*height_crop
    pix = crop.load()

    for i in range(0,height_crop,GRID_BOX_SIZE):
        for j in range(0,height_crop,GRID_BOX_SIZE):
            print(pix[0:2,0])
            grid_sum = sum(pix[i:GRID_BOX_SIZE,j:GRID_BOX_SIZE])
        

    height_foam = 2
    draw.text([0,0], text=height_foam, fill=(0,0,0))

    path, _ = image_path.split(".")
    new_name = path + 'proc.jpg'
    im.save(new_name)
    return height_foam

foam('images/pic0.jpg')
foam('images/pic1.jpg')