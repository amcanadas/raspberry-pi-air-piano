# -*- coding: utf-8 -*-
import pygame
from scikits.samplerate import resample
import util

class Notes:
    def __init__(self):
        self.scale_dict={}
        self.generate_scale()

    def generate_scale(self):
        """
        Given the initial note, middle C, create the rest of the musical scale by
        resampling.
    
        Returns: Dictionary of musical scale with the key being the name of the note
        and the value being the corresponding sound object.
    
        """    
        pygame.mixer.init()
    
        wav = util.get_app_path() + "res/piano-c.wav"
        sound = pygame.mixer.Sound(wav)
        
        pygame.mixer.set_num_channels(32)
        sndarray = pygame.sndarray.array(sound)

        ratio_dict = {'low_c': 1, 'c_sharp': .944, 'd': .891, 'd_sharp':.841, 'e':.794,
                  'f':.749, 'f_sharp': .707, 'g': .667, 'g_sharp': .63, 'a': .594,
                  'a_sharp': .561, 'b':.53, 'high_c':.5}
    
        # Generate the Sound objects from the dictionary.
        scale = {}
        for key,value in ratio_dict.iteritems():
            smp = resample(sndarray, value,"sinc_fastest").astype(sndarray.dtype)
            # Use the key, currently a string, as a variable
            scale[key] = pygame.sndarray.make_sound(smp)
            
        self.scale_dict=scale

    def play(self,note):
        print('Sound playing')
        self.scale_dict[note].play()
        
