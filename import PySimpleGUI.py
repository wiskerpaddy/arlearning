#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import cv2

class PyLayout:

    sg.theme('DarkAmber')

    # ウィンドウに配置するコンポーネント
    layout = [  [sg.Text('表示対象のファイルを指定してください',key='txtFileAllocate',enable_events=True)],
                [sg.Text('ファイル',key='txtFile',size=(15,1)), sg.Input(),sg.FileBrowse('ファイルを選択', key='inputFilePath')],
                [sg.Text('',key='txtSpaceFst',size=(63,1))],
                [sg.Button('マーカー保存',key='btnShw',size=(10,1)),
                 sg.Button('カメラ起動',key='btnActCmr',size=(10,1)), sg.Text('',key='txtSpaceScnd',size=(35,1)),sg.Button('閉じる',key='btnClose',size=(11,1))]
            ]

    # ウィンドウの生成
    window = sg.Window('ARマーカー', layout)

    def main(window):

        def arGenerator():
            aruco = cv2.aruco
            dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

            fileName = "/home/pi/Desktop/fileTran/ar.png"
            generator = aruco.drawMarker(dictionary, 0, 100)
            cv2.imwrite(fileName, generator)
            img = cv2.imread(fileName)
            #cv2.imshow('ArMarker',img)
            cv2.waitKey(0)

        def ConvImg(corners, i, img, convimg):
            x=int(corners[i][0][0][0])
            y=int(corners[i][0][0][1])
            w=int(corners[i][0][2][0]) - int(corners[i][0][0][0])
            h=int(corners[i][0][2][1]) - int(corners[i][0][0][1])
            if w > 0 and h > 0:
                convimg = cv2.resize(convimg,(w,h))
                img[y:y+h,x:x+w] = convimg
            return img

        def arReader(values):

            aruco = cv2.aruco #arucoライブラリ
            dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
            picPath = values[0]

            img1 = cv2.imread(picPath)
            cap = cv2.VideoCapture(0) #ビデオキャプチャの開始

            while True:
                ret, frame = cap.read() #ビデオキャプチャから画像を取得
                Height, Width = frame.shape[:2] #sizeを取得
                img = cv2.resize(frame,(int(Width),int(Height)))
                corners, ids, rejectedImgPoints = aruco.detectMarkers(img, dictionary) #マーカを検出
                aruco.drawDetectedMarkers(img, corners, ids, (0,255,0)) #検出したマーカに描画する
                try:
                    if corners != []:
                        for i in range(len(ids)):
                            if ids[i] == 0:
                                img = ConvImg(corners, i, img, img1)
                    cv2.imshow('drawDetectedMarkers', img) #マーカが描画された画像を表示

                    #キー押下で終了
                    key = cv2.waitKey(1) #キーボード入力の受付
                    if key != -1:
                        break

                except:
                    print("error")

            cap.release() #ビデオキャプチャのメモリ解放
            cv2.destroyAllWindows() #すべてのウィンドウを閉じる

        # イベントループ
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == 'btnClose':
                break

            elif event == 'btnShw':
                arGenerator()

            elif event == 'btnActCmr':
                #try:
                if values[0] != '':
                    print("画像が指定されました")
                    arReader(values)
                    values[0] == ''

                #except values[0] == '':
                else:
                    print("表示したい画像を指定してください")

        window.close()

    if __name__ == '__main__':
        main(window)