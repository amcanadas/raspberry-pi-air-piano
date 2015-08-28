# -*- coding: utf-8 -*-
import pygame
from util import *

class VirtualKeyboard:
    """
    A Virtual Piano Keyboard
    """
    def __init__(self,bounding_box):
        """
        Input:
        :bounding_box: list with 4 coordinates delimiting the keyboard
        """
        self.matrix_width = 3
        self.minimum_control_points = 2
        self.minimum_detected = 1
        self.bounding_box = bounding_box
        self.key_height = 0.20 #% of the bottom part of the key is valid
        self.keys = { key:{"pressed":False,"control_points":[],"detected":0} \
                      for key in scale}
        self._generate_test_points()


    def pressed(self,i):
        return self.keys[i]['pressed']

    def unpressed(self,i):
        return not self.keys[i]['pressed']

    def _point_between(self,x1,y1,x2,y2,relative_distance):
        x = x1 + relative_distance * (x2 - x1)
        y = y1 + relative_distance * (y2 - y1)
        return int(x),int(y)

    def _key_test_matrix(self,p1,p2,p3,p4):
        point_list = []
        for i in range(1,self.matrix_width+1):
            t_x1,t_y1=self._point_between(
                        p1[0],
                        p1[1],
                        p3[0],
                        p3[1],1/float(self.matrix_width+1)*i)
            t_x2,t_y2=self._point_between(
                        p2[0],
                        p2[1],
                        p4[0],
                        p4[1],1/float(self.matrix_width+1)*i)
            for j in range(1,self.matrix_width+1):
                point_list.append(self._point_between(
                        t_x1,
                        t_y1,
                        t_x2,
                        t_y2,1/float(self.matrix_width+1)*j))

        return point_list

    def _generate_test_points(self):
        x3,y3 = self.bounding_box[2][0],self.bounding_box[2][1]
        x4,y4 = self.bounding_box[3][0],self.bounding_box[3][1]
        x1,y1 = self._point_between(self.bounding_box[0][0],
                                    self.bounding_box[0][1],
                                    x3,y3,1-self.key_height)
        x2,y2 = self._point_between(self.bounding_box[1][0],
                                    self.bounding_box[1][1],
                                    x4,y4,1-self.key_height)
        #print(x1,y1,x2,y2,x3,y3,x4,y4)
        def _add_white_key(name,i):
            self.keys[name]['control_points']=self._key_test_matrix(
                self._point_between(x1,y1,x2,y2,1/8.0*i),
                self._point_between(x1,y1,x2,y2,1/8.0*(i+1)),
                self._point_between(x3,y3,x4,y4,1/8.0*i),
                self._point_between(x3,y3,x4,y4,1/8.0*(i+1)))
        _add_white_key('low_c',0)
        _add_white_key('d',1)
        _add_white_key('e',2)
        _add_white_key('f',3)
        _add_white_key('g',4)
        _add_white_key('a',5)
        _add_white_key('b',6)
        _add_white_key('high_c',7)

    def test(self, mask):
        for key,data in self.keys.iteritems():
            fg=0
            if len(data['control_points'])>0:
                for i in data['control_points']:
                    if mask[i[1],i[0]]>0:
                        fg+=1
            if fg>self.minimum_control_points:
                data['detected'] += 1
                if data['detected'] > self.minimum_detected:
                    data['pressed'] = True
            else:
                data['pressed'] = False
                data['detected'] = 0
