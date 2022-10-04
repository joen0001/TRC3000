from PIL import Image, ImageDraw, ImageFont
import numpy as np

def foam(image_path,GRID_BOX_SIZE=15, THRESHOLD = 15):
    im = Image.open(image_path) # Can be many different formats.
    width,height = im.size  # Get the width and hight of the image for iterating over
    pix = im.load()

    grid_avg = 0
    mat_avg = []
    change = []
    current_avg = 0-THRESHOLD
    for i in range(height):
        for j in range(GRID_BOX_SIZE):
            pixel = pix[j,i]
            grid_avg += sum(pixel)
        if i%GRID_BOX_SIZE == 0:
            grid_avg = round(grid_avg/(pow(GRID_BOX_SIZE,2)*3))
            mat_avg.append(grid_avg)
            if abs(current_avg-grid_avg) > THRESHOLD:
                change.append(i)  
                current_avg = grid_avg
            grid_avg = 0
        
    print(change)

    draw = ImageDraw.Draw(im)

    height_foam = '2'
    draw.text([0,0], text=height_foam, fill=(0,0,0))
    draw.line([width/2,0,width/2,height],fill=(0,0,0))
    for x in change[2:-1]:
        draw.line([0,x,width,x],fill=(0,0,0),width=10)

    path, _ = image_path.split(".")
    new_name = path + 'proc.jpg'
    im.save(new_name)
    return height_foam

foam('images/pic0.jpg')
foam('images/pic1.jpg')