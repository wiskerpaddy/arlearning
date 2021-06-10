#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
import cv2
aruco = cv2.aruco #arucoライブラリ


# Create gridboard, which is a set of Aruco markers
# the following call gets a board of markers 5 wide X 7 tall
gridboard = aruco.GridBoard_create(
        markersX=2,
        markersY=2,
        markerLength=0.05,
        markerSeparation=0.01,
        dictionary=aruco.Dictionary_get(aruco.DICT_4X4_50))

# Create an image from the gridboard
img = gridboard.draw(outSize=(210, 297))
cv2.imwrite("C:\\Users\\yuuki\\Desktop\\soft_learning\\test_gridboard.jpg", img)

# Display the image to us
cv2.imshow('Gridboard', img)
# Exit on any key
cv2.waitKey(0)
cv2.destroyAllWindows()