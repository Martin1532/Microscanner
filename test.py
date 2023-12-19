import sys
import cv2
import numpy as np
import os

# Function to stitch two images together
def stitch_images(image1, image2):
    img1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=2000)
    keypoints1, descriptors1 = orb.detectAndCompute(img1_gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(img2_gray, None)

    bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good.append(m)

    MIN_MATCH_COUNT = 10

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        def warpImages(img1, img2, H):
            rows1, cols1 = img1.shape[:2]
            rows2, cols2 = img2.shape[:2]

            list_of_points_1 = np.float32([[0, 0], [0, rows1], [cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
            temp_points = np.float32([[0, 0], [0, rows2], [cols2, rows2], [cols2, 0]]).reshape(-1, 1, 2)

            list_of_points_2 = cv2.perspectiveTransform(temp_points, H)

            list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)

            [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
            [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)

            translation_dist = [-x_min, -y_min]

            H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

            output_img = cv2.warpPerspective(img2, H_translation.dot(M), (x_max - x_min, y_max - y_min))
            output_img[translation_dist[1]:rows1 + translation_dist[1], translation_dist[0]:cols1 + translation_dist[0]] = img1

            return output_img

        return warpImages(image2, image1, M)

    return None

# Path to the folder containing images
image_folder = "Python\capture"

# List all image files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpg")]
image_files.sort()  # Ensure the files are sorted in the desired order

result = cv2.imread(os.path.join(image_folder, image_files[0]))

# Iterate through the image files and stitch them together
for i in range(1, len(image_files)):
    img = cv2.imread(os.path.join(image_folder, image_files[i]))
    
    # Check if the image loaded successfully
    if img is not None:
        if result is not None:
            result = stitch_images(result, img)
        else:
            print(f"Error: Failed to load or stitch image {image_files[i]}")
    else:
        print(f"Error: Failed to load image {image_files[i]}")

# Display the final stitched image if it is not empty
if result is not None:
    cv2.imshow("Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error: No valid stitched result to display")


# Display the final stitched image
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
