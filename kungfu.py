#!/usr/bin/env python

import random, os.path
import ConfigParser

#import basic pygame modules
import pygame
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


#game constants
SCREENRECT     = Rect(0, 0, 640, 480)

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


class dummysound:
    def play(self): pass

def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(main_dir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()

# This is the basic game object, we can create different game taget
# with it (read configuration from file)
class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 0
        self.images = {}

    def update(self):
        pass

# we'll manage all sprite groups in this class
class GroupManger():
    def __init__(self):
        self.groups = {}
        pass
    
    def group_init(self):
        pass

    def group_clean(self):
        pass

    def group_update(self):
        pass

    def group_draw(self):
        pass

# do init work and return sprite group
def init():
    pass

def main(winstyle = 0):
    # Initialize pygame
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

        #cap the framerate
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()


#call the "main" function if running this script
if __name__ == '__main__': main()

