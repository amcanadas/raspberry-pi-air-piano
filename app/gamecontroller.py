# -*- coding: utf-8 -*-
import math
import pygame, cv2
from pygame.locals import *
import notes, camera, circle
import util, virtualkeyboard
import rtopencv

class GameController:
    """
    Controls the Piano App (Game) status/behaviour
    """
    instance = None

    def __init__(self):
        self.running = True
        self.calibrating = False
        self.playing = False
        self.keyboard = None
        self.verbose=False
        self.play_status = { key:False for key in util.scale}
        self.picam=camera.Camera(util.config["camera_size"])
        # Window initialization FULLSCREEN
        self.screen=pygame.display.set_mode((1024,768))#,pygame.FULLSCREEN)
        # Load sound objects that will be used for key press
        self.sound = notes.Notes()
        self.background = self._draw_background()
        self._init_calibrating()
        self.fgmask = None
        self.last_frame = None
        self.last_fgmask = None
        GameController.instance = self

    @staticmethod
    def get_instance():
        return GameController.instance

    def _init_calibrating(self):
        self.calibrating_rect = pygame.sprite.Group()
        self.circles = {}
        self.circles["lefttop"] = circle.Circle(self.picam.pygame_position.left,self.picam.pygame_position.top,"lefttop")
        self.circles["righttop"] = circle.Circle(self.picam.pygame_position.right,self.picam.pygame_position.top,"righttop")
        self.circles["leftbottom"] = circle.Circle(self.picam.pygame_position.left,self.picam.pygame_position.bottom,"leftbottom")
        self.circles["rightbottom"] = circle.Circle(self.picam.pygame_position.right,self.picam.pygame_position.bottom,"rightbottom")
        self.calibrating_rect.add(self.circles.itervalues())

    def _draw_background(self):
        # Add background image
        pianoimage = pygame.image.load(util.get_app_path() + "/res/piano.jpg")
        image_width = 1024.0
        image_height = pianoimage.get_height()*(image_width/pianoimage.get_width())
        image_width = int(image_width)
        image_height = int(math.floor(image_height))
        pianoimage = pygame.transform.scale(pianoimage,(image_width,image_height))
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.blit(pianoimage, (0,0))
        # Text information to go to background
        if pygame.font:
            self.font = pygame.font.Font(None, 36)
            self.bigfont = pygame.font.Font(None, 64)
            self.smallfont = pygame.font.Font(None, 18)
            title = self.bigfont.render("Piano Sketch", 1, (0xCA,0xFF,0x70))
            by = self.smallfont.render("By: ChopSueyTeam", 1, (0xCA,0xFF,0x70))
            background.blit(title, title.get_rect(top=20, left=512-title.get_width()/2))
            background.blit(by, by.get_rect(top=700, left=1004-by.get_width()))

        return background

    def redraw(self):
        self.screen.blit(self.background, (0,0))
        if self.calibrating:
            util.pygame_camera_draw(self.picam)
            self.calibrating_rect.draw(self.screen)
            pygame.draw.line(self.screen,util.WHITE,
                             self.circles["lefttop"].rect.center,
                             self.circles["righttop"].rect.center)
            pygame.draw.line(self.screen,util.WHITE,
                             self.circles["lefttop"].rect.center,
                             self.circles["leftbottom"].rect.center)
            pygame.draw.line(self.screen,util.WHITE,
                             self.circles["righttop"].rect.center,
                             self.circles["rightbottom"].rect.center)
            pygame.draw.line(self.screen,util.WHITE,
                             self.circles["leftbottom"].rect.center,
                             self.circles["rightbottom"].rect.center)
            hint = self.font.render("Click on the circles and adjust to the piano keyboard zone", 1,(0xCA,0xFF,0x70))
            self.screen.blit(hint, hint.get_rect(top=600, left=20))
        if self.verbose and self.playing:
            if self.last_frame != None:
                self.screen.blit(self.last_frame,(0,0))
            if self.last_fgmask != None:
                mask_bgr = cv2.cvtColor(self.last_fgmask,cv2.COLOR_GRAY2BGR)
                mask = self.picam._to_pygame(mask_bgr)
                self.screen.blit(mask,(self.picam.width+5,0))
                for key, value in self.keyboard.keys.iteritems():
                    for pixel in value['control_points']:
                        if mask.get_at(pixel) == (255,255,255,255):
                            pygame.draw.circle(mask, (255,100,30), pixel, 2, 0)
                        else:
                            pygame.draw.circle(mask, (0,150,255), pixel, 2, 0)
                #pygame.draw.line(mask,util.GREEN,
                #             circles["leftbottom"].rect.center-picam.pygame_position,
                #             circles["rightbottom"].rect.center-picam.pygame_position)
                self.screen.blit(mask,(self.picam.width*2+10,0))
            hint = self.font.render("Verbose mode ON ({:.1f}fps average)".format(self.opencv.get_fps()),
                1,(0xCA,0xFF,0x70))
            self.screen.blit(hint, hint.get_rect(top=650, left=10))
        if self.playing:
            hint = self.font.render("Touch the sketch and play the piano", 1,(0xCA,0xFF,0x70))
            self.screen.blit(hint, hint.get_rect(top=600, left=10))

    def process_key(self, key):
        key = chr(key)
        if key == 'c':
            self.calibrating=not(self.calibrating)
            if self.calibrating:
                # refres screen every 50ms
                pygame.time.set_timer(USEREVENT+1, 50)
            else:
                pygame.time.set_timer(USEREVENT+1, 0)
        elif key == 'p':
            self.playing=not(self.playing)
            if self.playing:
                self.keyboard=virtualkeyboard.VirtualKeyboard(
                    [[s.rect.center[0]-self.picam.pygame_position.left,s.rect.center[1]-self.picam.pygame_position.top] for s in [self.circles["lefttop"],self.circles["righttop"],self.circles["leftbottom"],self.circles["rightbottom"]]])
                self.start_fgsegmentation(self)
                # refres screen every 500ms
                pygame.time.set_timer(USEREVENT+2, 500)
            else:
                pygame.time.set_timer(USEREVENT+2, 0)
                self.stop_fgsegmentation()
        elif key == 'v':
            self.verbose = not self.verbose
        elif key == 'a':
            self.sound.play('low_c')
        elif key == 'w':
            self.sound.play('c_sharp')
        elif key == 's':
            self.sound.play('d')
        elif key == 'e':
            self.sound.play('d_sharp')
        elif key == 'd':
            self.sound.play('e')
        elif key == 'f':
            self.sound.play('f')
        elif key == 'r':
            self.sound.play('f_sharp')
        elif key == 'h':
            self.sound.play('g')
        elif key == 'y':
            self.sound.play('g_sharp')
        elif key == 'j':
            self.sound.play('a')
        elif key == 'u':
            self.sound.play('a_sharp')
        elif key == 'k':
            self.sound.play('b')
        elif key == 'l':
            self.sound.play('high_c')
        elif key == 'q' or ord(key) == K_ESCAPE:
            self.running = False

    def test_frame(self):
        self.keyboard.test(self.fgmask)
        for k,v in self.keyboard.keys.iteritems():
            if v['pressed']:
                if self.play_status[k] == False:
                    self.sound.play(k)
                    self.play_status[k] = True
            else:
                self.play_status[k] = False

    def start_fgsegmentation(self, status):
        self.bgs_mog = cv2.BackgroundSubtractorMOG(
            util.config["bgs_mog_params"][0],
            util.config["bgs_mog_params"][1],
            util.config["bgs_mog_params"][2],
            util.config["bgs_mog_params"][3])#5, 3, 0.4, .
        self.opencv = rtopencv.RTOpenCV(self.picam.camera, GameController.process_image)

    # process de frame , rtopencv and frame are passed as parameters
    @staticmethod
    def process_image(rtopencv_class, frame):
        controller = GameController.get_instance()
        controller.fgmask = controller.bgs_mog.apply(frame,controller.fgmask,
            learningRate=util.config["bgs_mog_params"][3])
        controller.test_frame()
        if controller.verbose:
            controller.last_frame = controller.picam._to_pygame(frame)
            controller.last_fgmask = controller.fgmask

    def stop_fgsegmentation(self):
        self.opencv.close()
        self.bgs_mod = None
