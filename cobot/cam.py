import pyk4a
from pyk4a import Config, PyK4A
import numpy as np
import cv2

class azure_kinect:
    def __init__(self) -> None:
        self.k4a = PyK4A(
            Config(
                color_format=pyk4a.ImageFormat.COLOR_BGRA32,
                color_resolution=pyk4a.ColorResolution.RES_2160P,
                depth_mode=pyk4a.DepthMode.WFOV_UNBINNED,
                camera_fps=pyk4a.FPS.FPS_15,
                synchronized_images_only=True,
            )
        )
        self.k4a.start()
        
    def capture_img(self):
        while True:
            capture = self.k4a.get_capture()
            if np.any(capture.color):
                color_img = capture.color[:, :, :3]
                break
        
        return color_img