from PIL import Image

im = Image.open('images/pic0.jpg') # Can be many different formats.
pix = im.load()
width,height = im.size  # Get the width and hight of the image for iterating over
area = (width/4,height/4,width/4,height/4)
img = im.crop(area)
# pix[x,y] = value  # Set the RGBA Value of the image (tuple)
im.save('images/adj_pic0.jpg')