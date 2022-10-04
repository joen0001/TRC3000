from PIL import Image, ImageDraw, ImageFont
import numpy as np

def foam(image_path, GRID_BOX_SIZE=10, THRESHOLD = 50):
    im = Image.open(image_path) # Can be many different formats.
    width,height = im.size  # Get the width and hight of the image for iterating over

    area = (width/2-GRID_BOX_SIZE/2,0,width/2+GRID_BOX_SIZE/2,height)
    crop = im.crop(area)

    draw = ImageDraw.Draw(im)
    draw.rectangle(area, outline=(0,0,0), width=10)

    width_crop,height_crop = crop.size
    n = width_crop*height_crop
    pix = crop.load()

    grid_ind = 0
    val = 0
    while grid_ind*GRID_BOX_SIZE < height//GRID_BOX_SIZE:
        for i in range(GRID_BOX_SIZE*grid_ind,GRID_BOX_SIZE*((grid_ind+1)),1): # Height
            pixel = pix[i,width_crop/2]
            val += sum(pixel)
        
    print(val)

    height_foam = 2
    draw.text([0,0], text=height_foam, fill=(0,0,0))

    path, _ = image_path.split(".")
    new_name = path + 'proc.jpg'
    im.save(new_name)
    return height_foam

foam('images/pic0.jpg')
foam('images/pic1.jpg')