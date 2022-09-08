from PIL import Image

im = Image.open('images/pic0.jpg') # Can be many different formats.
pix = im.load()
x,y = im.size  # Get the width and hight of the image for iterating over
print (x, y)  # Get the RGBA Value of the a pixel of an image
pix[5] = (255,255)
# pix[x,y] = value  # Set the RGBA Value of the image (tuple)
im.save('images/adj_pic0.jpg')