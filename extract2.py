from PIL import Image

R = 0
G = 0
B = 0
BOX_SIZE = 200

im = Image.open('images/pic0.jpg') # Can be many different formats.
width,height = im.size  # Get the width and hight of the image for iterating over

area = (width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE)
im = im.crop(area)

width,height = crop.size
n = width*height
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

for i in range(width):
    for j in range(height):
        if abs(i-width) < 10:
            pix[i,j] = (R_avg,G_avg,B_avg)
        if abs(j-height) < 10:
            pix[i,j] = (R_avg,G_avg,B_avg)

im.save('images/adj_pic0.jpg')

# Bounding box for specific area
# Average Pixels to give basic color
# Dict for color values

# FOAMING
# Vertical pixel array
# Detect colour vs foam
# Foam height