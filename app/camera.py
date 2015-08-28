# -*- coding: utf-8 -*-
import io
import time
import threading
import picamera
import picamera.array
import numpy
import cv2
import pygame
import util


class Camera():
    '''
       OpenCv Camera Wrapper
    '''
    def __init__(self, size):
        self.size = self.width, self.height = size
        self.camera = picamera.PiCamera()
        self.camera.resolution = (self.width, self.height)
        self.camera.framerate = util.config["camera_framerate"]
        time.sleep(1)
        #avoid exposure/white balace changes
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = g

        self.pygame_position = pygame.Rect(1024/2-self.width/2,768/2-self.height/2,
                                           self.width,self.height)
        self.image = None

    def _to_pygame(self,frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = numpy.rot90(m=frame,k=3)
        frame = numpy.fliplr(frame)
        frame = pygame.surfarray.make_surface(frame)
        return frame

   # get an pygame image
    def get_pygame_image(self):
        frame=self.get_image()
        return self.pygame_position, self._to_pygame(frame)

    # get an opencv image
    def get_image(self,image_format='bgr'):
        with picamera.array.PiRGBArray(self.camera) as stream:
            self.camera.capture(stream, format=image_format,use_video_port=True)
            self.image = stream.array
            return self.image

    def close(self):
        self.camera.close()
