import cv2
import numpy as np
import os
from PIL import Image

from typing import Optional, Tuple

from ultralytics import YOLO

# Mode
MODE = 'detect'

# 작업 경로
MODEL_NAME = 'train/weights/best.pt'
MODEL_PATH = os.path.join(MODE, MODEL_NAME)

WORK_DIR = ''

VAR_MODEL_DIR = WORK_DIR + MODEL_PATH # 모델이 저장된 경로
VAR_RES_DIR = WORK_DIR + 'result' # 실행 결과를 저장할 경로
VAR_SNAP_DIR = WORK_DIR + 'data' # 촬영 이미지를 저장할 경로

m_path = VAR_MODEL_DIR
r_path = VAR_RES_DIR
d_path = VAR_SNAP_DIR

class Visualization():
    def __init__(self, path): # Load a model
        self.model = YOLO(path)
    
    def run_on_image(self, img):
        image = Image.fromarray(img[..., ::-1]) 

        # 현재 이미지 크기 얻기
        width, height = image.size

        # Crop 범위 계산 (가로 크기를 15%에서 85% 사이로 crop)
        crop_left = width * 0.15
        crop_right = width * 0.85
        crop_top = 0
        crop_bottom = height

        # Crop 수행
        cropped_image = image.crop((crop_left, crop_top, crop_right, crop_bottom))
    
        target_size = (640, 640)
        resized_image = cropped_image.resize(target_size)
            
        source = resized_image
        results = self.model.predict(source, imgsz=640, conf=0.75)
          
        return results[0]

if __name__ == "__main__":
    print('test mode')
    vs = Visualization(m_path)
    
    fnames = os.listdir(d_path)
    idx = 0
    for fname in fnames:
        f_name, f_ext = os.path.splitext(fname)
        filename = os.path.join(d_path, fname)

        if (f_ext != '.jpg' and f_ext != '.JPEG'): continue
        
        print('img ', idx)
        print('filename: ', filename)
        
        img = cv2.imread(filename)
        
        result = vs.run_on_image(img, idx)

        idx += 1
        
        # Process results list
        names = result.names # A dictionary of class names. 
        boxes = result.boxes # A Boxes object containing the detection bounding boxes.
        img = result.plot() # Plots the detection results. Returns a numpy array of the annotated image.

        cv2.imshow('result', img)
        key = cv2.waitKey(0)
        
        if key == ord('q'):
            break

        elif key == ord(' '):
            pass
        
    print('test done')