from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Function to get the RGB color of the centre marked box in image
# Box is supposed to contain the non-foam section of liquid
def color(image_path, BOX_SIZE=200):
    # To centre box, size/2 on each side of centre
    BOX_SIZE = BOX_SIZE/2
    # Initialising Variables
    R = 0
    G = 0
    B = 0

    im = Image.open(image_path)
    # Width and hight of the image
    width,height = im.size  

    # Cropping the centre box area to watch
    area = (width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE)
    crop = im.crop(area)
    draw = ImageDraw.Draw(im)
    draw.rectangle([width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE], outline=(R,G,B), width=10)

    # Width and hight of the cropped image for iterating over
    width_crop,height_crop = crop.size
    n = width_crop*height_crop
    pix = crop.load()

    # Checking each pixel's RGB values and adding them separately
    for i in range(width_crop):
        for j in range(height_crop):
            pixel = pix[i,j]
            R += pixel[0]
            G += pixel[1]
            B += pixel[2]

    # Calculating average of each R,G,B value
    R = round(R/n)
    G = round(G/n)
    B = round(B/n)
    colour = (R,G,B)
    
    # 
    draw.text([20,20], text=colour, fill=(0,0,0))

    path, _ = image_path.split(".")
    new_name = path + 'proc_color.jpg'
    im.save(new_name)
    return colour
