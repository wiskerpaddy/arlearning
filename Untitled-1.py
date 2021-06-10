#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob

aruco = cv2.aruco #arucoライブラリ
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
gridboard = aruco.GridBoard_create(
        markersX=2,
        markersY=2,
        markerLength=0.05,
        markerSeparation=0.01,
        dictionary=aruco.Dictionary_get(aruco.DICT_4X4_50))

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
images = glob.glob('*.jpg')
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

def arReader():
    cap = cv2.VideoCapture(0) #ビデオキャプチャの開始
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        while True:

            ret, frame = cap.read() #ビデオキャプチャから画像を取得
            if ret == True:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2)

            Height, Width = frame.shape[:2] #sizeを取得

            img = cv2.resize(frame,(int(Width),int(Height)))

            corners, ids, rejectedImgPoints = aruco.detectMarkers(img, dictionary) #マーカを検出
            
            aruco.drawDetectedMarkers(img, corners, ids, (0,255,0)) #検出したマーカに描画する

            cameraMatrix,distCoeffs,rvec,tvec = cv2.calibrateCamera()
            valid = cv2.estimatePoseBoard(corners, ids, gridboard, cameraMatrix, distCoeffs, rvec, tvec)

            if valid > 0:
                cv2.aruco.drawAxis(	img, cameraMatrix, distCoeffs, rvec, tvec, 0.1)
            
            cv2.imshow('drawDetectedMarkers', img) #マーカが描画された画像を表示

            cv2.waitKey(1) #キーボード入力の受付

            cap.release() #ビデオキャプチャのメモリ解放
            cv2.destroyAllWindows() #すべてのウィンドウを閉じる

arReader()