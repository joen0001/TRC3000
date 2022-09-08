from PIL import Image

im = Image.open('images/pic0.jpg') # Can be many different formats.
pix = im.load()
width,height = im.size  # Get the width and hight of the image for iterating over

# #CROP
#area = (width/4,height/4,3*width/4,3*height/4)
#im = im.crop(area)

for i in range(width):
    for j in range(height):
        if (width/2-i)**2 > 100 and (height/2-j)**2 > 100:
            pix[i, j] = (255, 255, 255)

im.save('images/adj_pic0.jpg')

# Bounding box for specific area
# Average Pixels to give basic color
# Dict for color values

# FOAMING
# Vertical pixel array
# Detect colour vs foam
# Foam height
