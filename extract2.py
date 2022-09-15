from PIL import Image, ImageDraw, ImageFont
import numpy as np

def extract(image_path, BOX_SIZE=100):
    R = 0
    G = 0
    B = 0

    im = Image.open(image_path) # Can be many different formats.
    width,height = im.size  # Get the width and hight of the image for iterating over

    area = (width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE)
    crop = im.crop(area)

    width_crop,height_crop = crop.size
    n = width_crop*width_crop
    pix = crop.load()

    for i in range(width_crop):
        for j in range(height_crop):
            pixel = pix[i,j]
            R += pixel[0]
            G += pixel[1]
            B += pixel[2]

    R = round(R/n)
    G = round(G/n)
    B = round(B/n)

    draw = ImageDraw.Draw(im)
    draw.rectangle([width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE], outline=(R,G,B), width=10)

    if R > G + B:
        colour = 'Red'
    elif G > R + B:
        colour = 'Green'  
    elif B > R + G:
        colour = 'Blue'
    else:
        colour = 'Clear/White'

    font_size = ImageFont.truetype(size=20)
    draw.text([width/2-BOX_SIZE,height/2-BOX_SIZE-20], text=colour, font=font_size, fill=(R,G,B))

    path, _ = image_path.split(".")
    new_name = path + 'proc.jpg'
    im.save(new_name)


extract('images/pic0.jpg', BOX_SIZE=100)