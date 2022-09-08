from PIL import Image
import numpy as np

im = Image.open('images/pic0.jpg') # Can be many different formats.
pix = im.load()
width,height = im.size  # Get the width and hight of the image for iterating over

# #CROP
BOX_SIZE = 200
area = (width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE)
im = im.crop(area)
print(pix[0,0])
#avg = np.mean(pix)

im.save('images/adj_pic0.jpg')

# Bounding box for specific area
# Average Pixels to give basic color
# Dict for color values

# FOAMING
# Vertical pixel array
# Detect colour vs foam
# Foam height
