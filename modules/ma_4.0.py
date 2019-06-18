# -*- coding: utf-8 -*-
import cv2
import sys
import os
import datetime
from time import time
import time as tm
import threading
from multiprocessing import Process
from multiprocessing import Pool
import multiprocessing as multi
import paramiko
import scp as scp


class video_man():
    def __init__(self):
        #初期設定
        self.flag = 0
        self.video_flag = 0
        self.check_flag = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.before = None
        self.start = time()
        self.x,self.y = 1,1
        self.face_re = 0
        #self.p = Pool(multi.cpu_count())
        self.process_flag = 0
        self.jobs = []

    def check_timer(self):
        for i in 3:
            tm.sleep(0.5)
            if self.check_flag == 1:
                break
            else:
                self.video_flag = 1

    def face_check(self):
        #顔認証をカスケード分類機で行う.cascade_pathはかける特徴データを決める.この場合は正面から見た顔
        cascade_path = "haarcascade_frontalface_alt.xml"
        #cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_eye.xml"
        #ここで保存した写真を分類機にかけるという愚行を犯しているのでここは要変更
        image_path = "face_pic.jpg"
        color = (255, 255, 255)
        #ファイル読み込み
        image = cv2.imread(image_path)
        #グレースケール変換
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #カスケード分類器で特徴量を取得する
        cascade = cv2.CascadeClassifier(cascade_path)
        #物体認識（顔認識）の実行
        #image – matrix
        #objects – vector
        #scaleFactor – scale
        #minNeighbors – rectangle
        #flags – ???
        #minSize – too
        facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
        print("face rectangle")
        print(facerect)
        #大きいものを選択
        if len(facerect) > self.face_re:
            #create rectangle
            self.face_re = len(facerect)
            for rect in facerect:
                cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
                #save
            cv2.imwrite("detected.jpg", image)
        os.remove("face_pic.jpg")

    def main(self):
        #カメラ映像を取得するcapを生成
        cap = cv2.VideoCapture(0)
        while True:
            #capから映像を取得
            ret, frame = cap.read()
            #サイズを小さくする
            frame = cv2.resize(frame, (int(frame.shape[1]/4), int(frame.shape[0]/4)))
            cv2.imshow('Raw Frame', frame)

            #前フレームとの違いを見る(動体検知)
            #グレースケールに変換
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.before is None:
                self.before = gray.copy().astype('float')
                continue
            cv2.accumulateWeighted(gray, self.before, 0.5)
            mdframe = cv2.absdiff(gray, cv2.convertScaleAbs(self.before))
            #白黒変換。真っ白と真っ黒の画像にして真っ白があったらそれは動いているものとする
            thresh = cv2.threshold(mdframe, 3, 255, cv2.THRESH_BINARY)[1]

            image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            max_area = 0
            try:
                target = contours[0]
            except IndexError:
                pass
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if max_area < area and area < 10000 and area > 1000:
                    max_area = area
                    target = cnt

            if max_area <= 1000:
            	areaframe = frame

            else:
                #動体検知された時の処理
                self.start = time()
                #最初の動体検知.映像の録画を始めるところ
                if self.flag == 0:
                    print("動体検知後の起動")
                    self.flag = 1
                    d=datetime.datetime.now()
                    filerename = d.strftime('%Y:%m:%d:%H:%M:%S') + '.mp4'
                    fps = 10
                    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                    videoWriter = cv2.VideoWriter('output.mp4', fmt, fps, (480,360))
                    cv2.imwrite('detected.jpg',frame)
                x,y,w,h = cv2.boundingRect(target)
                areaframe = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.imwrite('face_pic.jpg',frame)
                if self.process_flag == 0:
                    p = Process(target=self.face_check)
                    self.jobs.append(p)
                    p.start()
                    self.process_flag = 1
                if self.jobs[-1].exitcode == 0:
                    self.process_flag = 0
                    self.jobs[-1].terminate()

            #cv2.imshow('MotionDetected Area Frame', areaframe)
            if self.flag == 1:
                print('rec')
                frame = cv2.resize(frame, (480, 360))
                # 書き込み
                videoWriter.write(frame)

                end=time()
                #動体検知後10秒間動くものが存在しなかった場合録画を終了
                if end-self.start >= 10:
                    self.flag = 2
            #録画したものの書き出し,親機への動画,画像の転送
            if self.flag == 2:
                os.rename('output.mp4','%s'%(filerename))
                videoWriter.release()
                filerename2 = str(today)+'.jpg'
                os.rename('detected.jpg','%s'%(filerename2))
                #sshを用いて親機へファイルを転送
                with paramiko.SSHClient() as ssh:
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname='parent IP',port=22,username='pi',password='pi password')
                    with scp.SCPClient(ssh.get_transport()) as scp2:
                        scp2.put(filerename,'~/Documents/SAL/viewer/public/movie')
                        scp2.put(filerename2,'~/Documents/SAL/viewer/public/picture')
                print("rest")
                tm.sleep(3)
                self.flag = 0
            k = cv2.waitKey(1)
            if k == 27:
                tm.sleep(3)
                break


        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    test = video_man()
    test.main()
