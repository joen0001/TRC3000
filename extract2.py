from PIL import Image, ImageDraw
import numpy as np

R = 0
G = 0
B = 0
BOX_SIZE = 200

im = Image.open('images/pic0.jpg') # Can be many different formats.
width,height = im.size  # Get the width and hight of the image for iterating over

area = (width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE)
crop = im.crop(area)

width_crop,height_crop = crop.size
n = width_crop*width_crop
pixel_data = np.array(crop.getdata())
R = round(np.mean(pixel_data[:][0]))
G = round(np.mean(pixel_data[:][1]))
B = round(np.mean(pixel_data[:][2]))
print(pixel_data[0])

print(np.mean(pixel_data[:][0]))
draw = ImageDraw.Draw(im)
draw.rectangle([width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE], outline=(0,0,0), width=10)



im.save('images/adj_pic0.jpg')

# Bounding box for specific area
# Average Pixels to give basic color
# Dict for color values

# FOAMING
# Vertical pixel array
# Detect colour vs foam
# Foam height
