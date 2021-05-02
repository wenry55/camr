import io
from PIL import Image
import select
import v4l2capture
import numpy as np
import cv2
from base_camera import BaseCamera
import time


class Camera(BaseCamera):
    """Requires python-v4l2capture module: https://github.com/gebart/python-v4l2capture"""

    video_source = "/dev/video0"

    @staticmethod
    def frames():
        video = v4l2capture.Video_device(Camera.video_source) 
        # Suggest an image size. The device may choose and return another if unsupported
        size_x = 1920 
        size_y = 1080 
        size_x, size_y = video.set_format(size_x, size_y,0)
        video.create_buffers(4)
        video.queue_all_buffers()
        video.start()
        bio = io.BytesIO()

        yuv = np.empty((1920*1080)*3, dtype=np.uint8)
        try:
            while True:
                select.select((video,), (), ())  # Wait for the device to fill the buffer.
                image_data = video.read_and_queue()
                img = np.frombuffer(image_data,dtype=np.uint8)
                y=img[1::2]
                u=img[0::4]
                v=img[2::4]

                yuv[::3] = y
                yuv[1::6] = u
                yuv[2::6] = v
                yuv[4::6] = u
                yuv[5::6] = v
                image = Image.frombytes("YCbCr",(size_x,size_y),yuv)
                resize_image = image.resize((640,380))
                resize_image.save(bio, format="jpeg")
                yield bio.getvalue()
                bio.seek(0)
                bio.truncate()
                time.sleep(0.1)
        finally:
            video.close()
