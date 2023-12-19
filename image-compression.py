from PIL import image
import PIL
import os
import glob

im = Image.open("image-1.jpg")
im = Image.open("D:\Neurabot\Microscanner\V2\Pemrograman\Python\image\temp1655872425773\image-1.jpg")
print(f"The image size dimensions are: {im.size}")

file_name = 'image-1-compressed.jpg'
picture = Image.open('image-1.jpg')
dim = picture.size
print(f"This is the current width and height of the image: {dim}")
picture.save("Compressed_"+file_name,optimize=True,quality=30) 