# -*- coding: utf-8 -*-
"""
Lyght Piano
amcanadas@gmail.com


Dependencies:
Python 2.7
NumPy, SciPy, PyGame, Scikits.samplerate, OpenCV
"""

import sys, os, time
import numpy, pygame
from pygame.locals import *
import camera , virtualkeyboard
import util, gamecontroller


def main():
    util.read_config()
    pygame.mixer.pre_init(44100,-16,1,1024*1)
    pygame.init()
    controller = gamecontroller.GameController()
    pygame.display.update()

    def process_events(events, controller):
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            if event.type == MOUSEMOTION:
                for b in controller.circles.itervalues():
                    if (b.is_pressed):
                        b.rect.move_ip(event.rel)
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = [s for s in controller.circles.itervalues() if s.rect.collidepoint(pos)]
                for b in clicked:
                    b.pressed()
            if event.type == MOUSEBUTTONUP:
                for b in controller.circles.itervalues():
                    b.unpressed()
            if event.type == USEREVENT + 1:
                #only redraw needed
                pass
            if event.type == USEREVENT + 2:
                #only redraw needed
                pass
            if event.type == KEYDOWN:
                controller.process_key(event.key)


    while controller.running:
        process_events([pygame.event.wait()]+pygame.event.get(), controller)

        controller.redraw()

        pygame.display.flip()

    if controller.playing:
        controller.stop_fgsegmentation()
    controller.picam.close()
    pygame.quit()

if __name__ == "__main__":
    main()
