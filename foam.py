from PIL import Image, ImageDraw, ImageFont
import numpy as np

def foam(image_path,GRID_BOX_SIZE=10, THRESHOLD = 60):
    DISTANCE_SCALAR = 0.1
    im = Image.open(image_path) # Can be many different formats.
    width,height = im.size  # Get the width and hight of the image for iterating over
    pix = im.load()

    grid_avg = 0
    mat_avg = []
    change = []
    current_avg = 0-THRESHOLD
    for i in range(height):
        pixel = pix[width/2,i]
        grid_avg += sum(pixel)
        if i%GRID_BOX_SIZE == 0:
            grid_avg = round(grid_avg/(GRID_BOX_SIZE*3))
            mat_avg.append(grid_avg)
            if abs(current_avg-grid_avg) > THRESHOLD:
                change.append(i)  
                current_avg = grid_avg
            grid_avg = 0

    draw = ImageDraw.Draw(im)

    draw.line([width/2,0,width/2,height],fill=(0,0,0))

    heights = []
    for i in range(1,len(change)):
        height_section = (change[i]-change[i-1])*DISTANCE_SCALAR
        heights.append(height_section)
        draw.line([0,change[i],width,change[i]],fill=(255,255,255),width=10)
        draw.text([0,change[i]], text=str(height_section), fill=(0,0,0))

    height_foam = heights[1]
    path, _ = image_path.split(".")
    new_name = path + 'proc_foam.jpg'
    im.save(new_name)
    return height_foam
