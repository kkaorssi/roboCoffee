import cv2
import numpy as np
from PIL import Image

from ultralytics import YOLO

class Visualization():
    def __init__(self):
        self.model = YOLO('detect/train/weights/best.pt')

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