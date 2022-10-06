from PIL import Image, ImageDraw, ImageFont
import numpy as np

def extract(image_path, BOX_SIZE=80,GRID_BOX_SIZE=10,THRESHOLD = 25):
    BOX_SIZE = BOX_SIZE/2
    R = 0
    G = 0
    B = 0

    im = Image.open(image_path) # Can be many different formats.
    width,height = im.size  # Get the width and hight of the image for iterating over

    area = (width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE)
    crop = im.crop(area)
    

    width_crop,height_crop = crop.size
    n = width_crop*height_crop
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

    if R > G + B:
        colour = 'Red: ' + str([R,G,B])
    elif G > R + B:
        colour = 'Green: ' + str([R,G,B])
    elif B > R + G:
        colour = 'Blue: ' + str([R,G,B])
    else:
        colour = 'Clear/White + ' + str([R,G,B])

    # FOAMING
    pix = im.load()
    grid_avg = 0
    mat_avg = []
    change = []
    current_avg = 0-THRESHOLD
    for i in range(height):
        pixel = pix[width/2,i]
        grid_avg += sum(pixel)
        if i % GRID_BOX_SIZE == 0:
            grid_avg = round(grid_avg/(GRID_BOX_SIZE*3))
            mat_avg.append(grid_avg)
            if abs(current_avg-grid_avg) > THRESHOLD:
                change.append(i)  
                current_avg = grid_avg
            grid_avg = 0
    
    # DRAWING/OUTPUT
    draw = ImageDraw.Draw(im)
    draw.rectangle([width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE], outline=(R,G,B), width=4)
    draw.line([width/2,0,width/2,height],fill=(0,0,0))
    #for x in change:
    #    draw.line([0,x,width,x],fill=(0,0,0),width=4)
    draw.text([0,0], text=colour, fill=(R,G,B))

    path, _ = image_path.split(".")
    new_name = path + 'proc.jpg'
    im.save(new_name)
    return colour

extract('images/pic0.jpg')
extract('images/pic1.jpg')
