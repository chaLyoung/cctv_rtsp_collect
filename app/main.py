# -*- encoding: utf8 -*-
import cv2
import os
import json
import sys
import shutil
import uvicorn
import ftplib
import requests
import multiprocessing
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#TODO
# 서버로 띄울거면 FASTAPI 고려 (Docker 파일 바꾸어주어야 함
# app = FastAPI()
# origins = [
#     "*"
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# LOCAL_PORT = 9999

# @app.api_route("/startStream", methods=['GET', 'POST'])
# def mainTest():
#     print('init')


def startStream():  # 비동기로 함수 변경 요망
    # cap = cv2.VideoCapture("rtsp://admin:fron9116!!!@1.223.42.198:558/LiveChannel/1/media.smp") # HANHWA TECHWIN
    cap = cv2.VideoCapture("rtsp://admin:aistudio1@@192.168.1.71:554/ISAPI/streaming/channels/101") # HIKVISION
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    30 if fps >= 30 else fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    now = datetime.now()
    # print(width, height, fps)
    # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # fourcc = cv2.VideoWriter_fourcc(*'X264')
    avi_name = os.path.join(os.getcwd(), now.strftime('%Y%m%d%H%M%S') + '.avi') # 저장할 위치 지정
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    output = cv2.VideoWriter(avi_name, fourcc, fps, (width, height))
    
    while True:
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        # cv2.imshow('video', frame)
        output.write(frame)
        if cv2.waitKey(1) == 27:    # 제거해야 함
            break
        
        # 특정 시간에 loop 종료 메서드 작성
        
    cap.release()
    output.release()
    cv2.destroyAllWindows()

    name = os.path.splitext(avi_name)[0]
    mp4_name = name + ".mp4"
    try:
        os.system(f"ffmpeg -i {avi_name} {mp4_name}")
    except Exception as e:
        print("while convertion mp4 exception: " + str(e))


if __name__ == '__main__':
    startStream()
#     service_start()


# fastapi - uvicorn 로컬에서 실행할때만 필요
# def service_start():
#     global LOCAL_PORT
#
#     # if sys.platform.startswith('win'):
#     multiprocessing.freeze_support()
#
#     uvicorn.run(app, host="0.0.0.0", port=LOCAL_PORT)
