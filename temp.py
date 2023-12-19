# # import os

# # dir = 'sample tile image'

# # files = os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), dir))

# # # print(os.path.dirname(os.path.realpath(__file__)))

# # for f in files:
# # 	print(f)

# import os


# dir = 'image/temp1639373802626'
# mypath = os.path.join(os.path.dirname(os.path.realpath(__file__)), dir)
# onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

# col = []
# row = []
# for file in onlyfiles:
#    file = file.split(".")[0]
#    split= file.split('_')
#    # print(split[0])
#    col.append(int(split[0]))
#    row.append(int(split[1]))

# print(max(col))
# print(max(row))
# # col.sort()
# # print(*col)


import cv2
import os

os.chdir(r'D:\Neurabot\Microscanner\V2\Pemrograman\Python')
cap = cv2.imread('test.jpg')

if (cap is None):
    print('img not found')
else:
    print('img exist')

# cv2.imshow('img', cap)
