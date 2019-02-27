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
        cascade_path = "haarcascade_frontalface_alt.xml"
        #cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_eye.xml"
        image_path = "face_pic.jpg"
        color = (255, 255, 255) #白
        #ファイル読み込み
        image = cv2.imread(image_path)
        #グレースケール変換
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #カスケード分類器の特徴量を取得する
        cascade = cv2.CascadeClassifier(cascade_path)
        #物体認識（顔認識）の実行
        #image – matrix
        #objects – vector
        #scaleFactor – scale
        #minNeighbors – rectangle
        #flags – ???
        #minSize – too

        #facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1,1))
        facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
        print("face rectangle")
        print(facerect)
        if len(facerect) > self.face_re:
            #create rectangle
            self.face_re = len(facerect)
            for rect in facerect:
                cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
                #save
            cv2.imwrite("detected.jpg", image)
        os.remove("face_pic.jpg")

    def main(self):
        cap = cv2.VideoCapture(0)
        while True:
            #read camera
            ret, frame = cap.read()

            # size change
            frame = cv2.resize(frame, (int(frame.shape[1]/4), int(frame.shape[0]/4)))
            # default frame
            #show! show! show!
            cv2.imshow('Raw Frame', frame)

            # difference
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.before is None:
                self.before = gray.copy().astype('float')
                continue

            cv2.accumulateWeighted(gray, self.before, 0.5)
            mdframe = cv2.absdiff(gray, cv2.convertScaleAbs(self.before))

            # 動いているところが明るい画像を表示する
            #cv2.imshow('MotionDetected Frame', mdframe)
            thresh = cv2.threshold(mdframe, 3, 255, cv2.THRESH_BINARY)[1]

            image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            max_area = 0
            try:
                target = contours[0]
            except IndexError:
                pass
                #print('Nothing')
            for cnt in contours:

                area = cv2.contourArea(cnt)
                if max_area < area and area < 10000 and area > 1000:
                    max_area = area;
                    target = cnt

            if max_area <= 1000:
            	areaframe = frame

            else:
                self.start = time()
                if self.flag == 0:
                    print("ここで動体検知後の起動ができそう")
                    self.flag = 1
                    d=datetime.datetime.now()
                    #today = str(d.year) + ':' + str(d.month) + ':' + str(d.day) + ':' + str(d.hour) + ':' + str(d.minute) + ':' + str(d.second)
                    #filerename=str(today)+'.mp4'
                    filerename = d.strftime('%Y:%m:%d:%H:%M:%S') + '.mp4'
                    fps = 10
                    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                    videoWriter = cv2.VideoWriter('output.mp4', fmt, fps, (480,360))
                    cv2.imwrite('detected.jpg',frame)
                x,y,w,h = cv2.boundingRect(target)
                areaframe = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.imwrite('face_pic.jpg',frame)
                if self.process_flag == 0:
                    #self.p.starmap(self.face_check) 
                    p = Process(target=self.face_check)
                    self.jobs.append(p)
                    p.start()
                    '''
                    #self.p.join()
                    '''
                    self.process_flag = 1
                if self.jobs[-1].exitcode == 0:
                    self.process_flag = 0
                    self.jobs[-1].terminate()

            cv2.imshow('MotionDetected Area Frame', areaframe)
            #print(self.process_flag)
            if self.flag == 1:
                print('rec')
                # 圧縮
                frame = cv2.resize(frame, (480, 360))
                # 書き込み
                videoWriter.write(frame)

                end=time()
                if end-self.start >= 10:
                    self.flag = 2
            if self.flag == 2:
                os.rename('output.mp4','%s'%(filerename))
                videoWriter.release()
                filerename2 = str(today)+'.jpg'
                os.rename('detected.jpg','%s'%(filerename2))
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
                tm.sleep(1)
                break


        cap.release()
        cv2.destroyAllWindows()

test = video_man()
test.main()
