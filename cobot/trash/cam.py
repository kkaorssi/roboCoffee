import cv2
import os
import numpy as np
import pandas as pd

# from cobot.detect import Visualization
from detect import Visualization

## communication message
MSG_CAM_READY = 0
MSG_TRIGGER = 1
MSG_PROG_STOP = 2
MSG_DETECTED = 3
MSG_NOTHING = 4

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

def kinect(conn):
    import pyk4a
    from pyk4a import Config, PyK4A
    
    vs = Visualization(m_path)
    
    cv2.namedWindow('color', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('color', 800, 600)
    
    k4a = PyK4A(
        Config(
            color_format=pyk4a.ImageFormat.COLOR_BGRA32,
            color_resolution=pyk4a.ColorResolution.RES_2160P,
            depth_mode=pyk4a.DepthMode.WFOV_UNBINNED,
            camera_fps=pyk4a.FPS.FPS_15,
            synchronized_images_only=True,
        )
    )
    k4a.start()
    
    idx = 0
    while 1:
        capture = k4a.get_capture()
        if np.any(capture.color) and np.any(capture.depth):
            color_img = capture.color[:, :, :3]
            depth_img = capture.depth
            
        # Plot the image
        cv2.imshow('color', color_img)
        key = cv2.waitKey(1) & 0xFF
        
        if conn:
            if conn.poll():
                robot_msg = conn.recv()
                if robot_msg == 'trigger':
                    key = ord(' ')
                elif robot_msg == 'stop':
                    key = ord('q')
        
        # Press q key to stop
        if key == ord('q'):
            break
        
        elif key == ord(' '):
            
            result = vs.run_on_image(color_img)
            
            # Process results list
            names = result.names # A dictionary of class names. 
            boxes = result.boxes.data # A Boxes object containing the detection bounding boxes.
            res_img = result.plot() # Plots the detection results. Returns a numpy array of the annotated image.
            
            drippers_df = pd.DataFrame(columns=['Name', 'Value1', 'Value2', 'Value3', 'Value4'])

            for n in range(len(boxes)):
                name = names[int(boxes[n][5])]
                values = boxes[n][0:4]
                
                new_row = pd.DataFrame({'Name': [name], 'Value1': [float(values[0])], 'Value2': [float(values[1])], 'Value3': [float(values[2])], 'Value4': [float(values[3])]})
                drippers_df = pd.concat([drippers_df, new_row], ignore_index=True)
    
            # 결과 확인
            print(drippers_df)

            conn.send(drippers_df)
            
            # 촬영된 이미지와 인식 결과 저장
            print("Saving image ", idx)
            os.makedirs(d_path, exist_ok=True)
            os.makedirs(r_path, exist_ok=True)
            
            fname_1 = 'orgimg_' + str(idx) + '.jpg'
            out_1 = os.path.join(d_path, fname_1)
            cv2.imwrite(out_1, color_img)

            fname_2 = 'orgdepth_' + str(idx) + '.png'
            out_2 = os.path.join(d_path, fname_2)
            cv2.imwrite(out_2, depth_img)
            
            fname_3 = 'resimg_' + str(idx) + '.jpg'
            out_3 = os.path.join(r_path, fname_3)
            cv2.imwrite(out_3, res_img)
            
            idx += 1
            
    cv2.destroyAllWindows()
    k4a.stop()
    
if __name__ == '__main__':
    print('test mode')
    kinect(None)
    print('test done')