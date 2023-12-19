import cv2
import numpy as np
import pyvips
import datetime
import os


startrow = 0
endrow = 9
startcolumn = 0
endcolumn = 10

# # startrow = 0
# # endrow = 20
# # startcolumn = 0
# # endcolumn = 50

os.chdir(r'D:\Neurabot\Microscanner\V2\Pemrograman\Python\image')
os.chdir(r'D:\Neurabot\Backup WSI\SGU\Image')

print(datetime.datetime.now())
# tiles = [pyvips.Image.new_from_file(f"malaria256/{x}_{y}.jpg", access="sequential")
#          for y in range(height) for x in range(width)]

tiles = [pyvips.Image.new_from_file(f"lkjnmb/{x}_{y}.jpg", access="sequential")
         for y in range(startrow, endrow) for x in range(startcolumn, endcolumn)]


# image = pyvips.Image.arrayjoin(tiles, across=width)

image = pyvips.Image.arrayjoin(tiles, across=endcolumn-startcolumn)
image.write_to_file("tesScanner.tif", compression="jpeg", tile=True)
# image.dzsave("../slide/dzi/02-HE-5")

# os.mkdir("../slide/dzi/02-HE-5")
# shutil.move("../slide/dzi/02-HE-5.dzi", "../slide/dzi/02-HE-5/02-HE-5.dzi")
# shutil.move("../slide/dzi/02-HE-5_files", "../slide/dzi/02-HE-5/02-HE-5_files")

# print(datetime.datetime.now())

# Extract tile image
# src = "ori.tif"
# # src = 'tiff/JP2K-33003-1.svs'
# image = pyvips.Image.new_from_file(src)
# image.dzsave("ori")
