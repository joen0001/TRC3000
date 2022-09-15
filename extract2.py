from PIL import Image, ImageDraw
import numpy as np

R = 0
G = 0
B = 0
BOX_SIZE = 100

im = Image.open('images/pic0.jpg') # Can be many different formats.
width,height = im.size  # Get the width and hight of the image for iterating over

area = (width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE)
crop = im.crop(area)

width_crop,height_crop = crop.size
n = width_crop*width_crop
pix = im.load()

for i in range(width):
    for j in range(height):
        pixel = pix[i,j]
        R += pixel[0]
        G += pixel[1]
        B += pixel[2]

R_avg = round(R/n)
G_avg = round(G/n)
B_avg = round(B/n)

draw = ImageDraw.Draw(im)
draw.rectangle([width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE], outline=(R,G,B), width=10)



im.save('images/adj_pic0.jpg')

# Bounding box for specific area
# Average Pixels to give basic color
# Dict for color values

# FOAMING
# Vertical pixel array
# Detect colour vs foam
# Foam height
