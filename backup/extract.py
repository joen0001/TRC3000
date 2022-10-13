from PIL import Image, ImageDraw, ImageFont
import numpy as np

def extract(image_path, BOX_SIZE=80,GRID_BOX_SIZE=10,THRESHOLD = 25):
    BOX_SIZE = BOX_SIZE/2
    R = 0
    G = 0
    B = 0

    # Open image from file path
    im = Image.open(image_path)
    # Get the width and hight of the image
    width,height = im.size 

    # Create area within image to check color
    area = (width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE)
    # New cropped version of image
    crop = im.crop(area)
    
    # New dimensions of cropped area
    width_crop,height_crop = crop.size
    n = width_crop*height_crop
    pix = crop.load()

    # Adding the individual R,G,B values
    for i in range(width_crop):
        for j in range(height_crop):
            pixel = pix[i,j]
            R += pixel[0]
            G += pixel[1]
            B += pixel[2]

    # Average individual channel values
    R = round(R/n)
    G = round(G/n)
    B = round(B/n)
    colour = [R,G,B]

    # FOAMING
    pix = im.load()
    grid_avg = 0
    mat_avg = []
    change = []
    
    # Threshold to determine if there is a different layer
    current_avg = 0-THRESHOLD
    
    # Iterating over height
    for i in range(height):
        # Summing the values of grid_box_size in a column to be averaged
        pixel = pix[width/2,i]
        grid_avg += sum(pixel)
        
        if i % GRID_BOX_SIZE == 0:
            # Taking the average pixel values of each section
            grid_avg = round(grid_avg/(GRID_BOX_SIZE*3))
            mat_avg.append(grid_avg)
            
            # If the difference in average pixel values per section is greater than threshold,
            # Count changes as a different section
            if abs(current_avg-grid_avg) > THRESHOLD:
                change.append(i)  
                current_avg = grid_avg
            grid_avg = 0
    
    # DRAWING/OUTPUT
    draw = ImageDraw.Draw(im)
    # Draw bounding box used for color analysis
    draw.rectangle([width/2-BOX_SIZE,height/2-BOX_SIZE,width/2+BOX_SIZE,height/2+BOX_SIZE], outline=(0,0,0), width=4)
    
    # Output Specific RGB Colour values + Background box
    draw.rectangle([0,0,200,15], (255,255,255), width=-1)
    draw.text([0,0], text=str(colour), fill=(R,G,B))
    
    # Draw Lines at each new section
    draw.line([width/2,0,width/2,height],fill=(0,0,0))
    for x in change:
        draw.line([0,x,width,x],fill=(0,0,0),width=4)
    
    # Save processed image under new name
    path, _ = image_path.split(".")
    new_name = path + 'proc.jpg'
    im.save(new_name)
    return colour

# Run for these two pictures
extract('images/pic0.jpg')
extract('images/pic1.jpg')
