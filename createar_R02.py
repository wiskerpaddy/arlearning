#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import cv2
import traceback

sg.theme('DarkAmber')

# ウィンドウに配置するコンポーネント
layout = [  [sg.Text('表示対象のファイルを指定してください',key='txtFileAllocate')],
            [sg.Text('保存先フォルダ',key='arTxtFile',size=(15,1)),
             sg.InputText(key='fold'),
             sg.FolderBrowse('フォルダを選択',key='inputFolderPathMk')],
            [sg.Text('画像ファイル',key='txtFile',size=(15,1)),
             sg.InputText(key='filePathImg',enable_events=True),
             sg.FileBrowse('ファイルを選択',key='inputFilePath')],
            [sg.Text('カメラ番号',key='camera',size=(15,1)),
             sg.InputText(default_text='0',key='bangou')],
            [sg.Text('',key='txtSpaceFst',size=(63,1))],
            [sg.Button('マーカー保存',key='btnShw',size=(10,1)),
             sg.Button('カメラ起動',key='btnActCmr',size=(10,1)),
             sg.Text('',key='txtSpaceScnd',size=(35,1)),
             sg.Button('閉じる',key='btnClose',size=(11,1))]
        ]

# 表示するメッセージを格納する配列
mssge = {'null':'aiueo',
         'sucRsvMk':'マーカーが保存されました',
         'failDsgntMk':'マーカーの保存先を指定してください',
         'failDsgntImg':'表示したい画像を指定してください',
         'failDsgntMkPath':'マーカーの保存先Pathは「半角英数字」にしてください',
         'failDsgntImgPath':'画像の保存先Pathは「半角英数字」にしてください'}

# ウィンドウの生成
window = sg.Window('ARマーカー', layout)

def check_camera_connection(camera_bangou):

    error=0

    try:
        bangou=int(camera_bangou) + 1
    except ValueError:
        bangou=11

    if bangou==11:
        sg.popup("カメラ番号が数値ではありません。")
        error=1

    true_camera_is = []
    for camera_number in range(0,10):
        cap = cv2.VideoCapture(camera_number)
        ret,frame = cap.read()
        if ret is True:
            true_camera_is.append(camera_number)

    if len(true_camera_is)==0:
        sg.popup("カメラを接続してください。")
        error=1

    if len(true_camera_is) != bangou:
        sg.popup("カメラ番号が不一致です。")
        error=1

    #sg.popup("カメラ台数は、" + str(len(true_camera_is)) + "台です。")
    cap.release()
    cv2.destroyAllWindows()
    return error

# ARマーカーを生成する関数
def arGenerator(values):
    aruco = cv2.aruco
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    mkrPathFst = values['fold']
    mkrPathSec = "\\ar.png"
    mkrPath = mkrPathFst + mkrPathSec

    generator = aruco.drawMarker(dictionary, 0, 100)
    cv2.imwrite(mkrPath, generator)# ARマーカー指定した場所に保存する
    cv2.waitKey(0)

# 表示する画像サイズを整形する関数
def ConvImg(corners, i, img, convimg):
    x=int(corners[i][0][0][0])
    y=int(corners[i][0][0][1])
    w=int(corners[i][0][2][0]) - int(corners[i][0][0][0])
    h=int(corners[i][0][2][1]) - int(corners[i][0][0][1])
    if w > 0 and h > 0:
        convimg = cv2.resize(convimg,(w,h))
        img[y:y+h,x:x+w] = convimg
    return img

# ARマーカーカメラで読み取る関数
def arReader(values):

    aruco = cv2.aruco
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50) #マーカーサイズを指定
    picPath = values['filePathImg'] #表示する画像のpathを指定
    img1 = cv2.imread(picPath)

    #from IPython.core.debugger import Pdb; Pdb().set_trace()
    try:
        x=int(values['bangou'])
    except ValueError:
        x=0

    cap = cv2.VideoCapture(x)

    while True:
        ret, frame = cap.read()
        Height, Width = frame.shape[:2]
        img = cv2.resize(frame,(int(Width),int(Height)))
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img, dictionary)
        aruco.drawDetectedMarkers(img, corners, ids, (0,255,0))
        try:
            if corners != []:
                for i in range(len(ids)):
                    # 以下に要素を追加すれば複数の画像が表示可能
                    if ids[i] == 0:
                        img = ConvImg(corners, i, img, img1)
            cv2.imshow('drawDetectedMarkers', img)

            # 何かしらのキー押下で終了
            key = cv2.waitKey(1)
            if key != -1:
                break

        except:
            # 画像の表示に失敗したら原因を表示
            traceback.print_exc()

    cap.release()
    cv2.destroyAllWindows()

# main関数
def main(window):
    # イベントループ
    while True:
        event, values = window.read()


        # 閉じるボタンを押したらwindowを閉じる
        if event == sg.WIN_CLOSED or event == 'btnClose':
            break

        # マーカー保存ボタンを押したらARマーカーを保存する
        elif event == 'btnShw':

            # ARマーカーの保存先pathが空白か全角が入っていなかったらARマーカーを指定pathに保存する
            if values['fold'] != '':
                from IPython.core.debugger import Pdb; Pdb().set_trace()
                if values['fold'].encode('utf-8').isalnum() == True or values['fold'].encode('utf-8').isalnum() == False:
                    arGenerator(values)
                    sg.popup(mssge['sucRsvMk'])
                else:
                    sg.popup(mssge['failDsgntMkPath'])
                    #window['folderPathMk'].update(mssge['null'])
                    values['fold'] == ''
            else:
                sg.popup(mssge['failDsgntMk'])

        # カメラ起動ボタンを押したらカメラを起動する
        elif event == 'btnActCmr':

            camera_bangou=values['bangou']
            error = check_camera_connection(camera_bangou)

            if values['fold'] != '' and error==0:
               # 表示する画像のpathに空白か全角が入っていなかったら画像をマーカー上に表示する
                if values['filePathImg'] != '':
                    if values['filePathImg'].encode('utf-8').isalnum() == True or values['filePathImg'].encode('utf-8').isalnum() == False:
                        arReader(values)
                        values['filePathImg'] == ''
                    else:
                        sg.popup(mssge['failDsgntImgPath'])
                        values['filePathImg'] == ''
                else:
                    sg.popup(mssge['failDsgntMk'])
            else:
                sg.popup(mssge['failDsgntMk'])

    window.close()

if __name__ == '__main__':main(window)