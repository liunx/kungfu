#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""


#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

# __file__ python's internal variables
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#functions to create our resources
def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
        colorkey = surface.get_at((0,0))
        surface.set_colorkey(colorkey, RLEACCEL)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

# initializer for class GameObject
def object_init():
    """ the single image as default """
    GameObject.single_image = load_image('stand-still.png')
    GameObject.image_dict[K_h] = load_images('left-fist.png')
    GameObject.image_dict[K_l] = load_images('right-fist.png')
    GameObject.image_dict[K_j] = load_images('left-kick.png')
    GameObject.image_dict[K_k] = load_images('right-kick.png')
   

#classes for our game objects
class GameObject(pygame.sprite.Sprite):
    speed = 10
    animcycle = 12
    images = []
    single_image = None
    image_dict = {}
    """ add a new sprite """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.image = self.single_image
        self.images.append(self.single_image)
        self.rect = self.image.get_rect()
        self.frame = 0
        self.images_len = 1

    def update(self):
        """ show our sprite up """
        self.frame = self.frame + 1
        self.image = self.images[self.frame // self.animcycle % len(self.images)]

    def move(self, direct_x, direct_y):
        """ move the player """
        self.rect.move_ip(direct_x * self.speed, direct_y * self.speed);

    def get_key(self, key):
        """ get user input and reponse in actions """
        if key in self.image_dict:
            self.images = []
            self.images = self.image_dict[key]

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Elves-wood')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    object_init()
    game_obj = GameObject()
    allsprites = pygame.sprite.RenderPlain((game_obj))

#Main Loop
    going = True
    while going:
        clock.tick(60)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN:
                game_obj.get_key(event.key)

        allsprites.update()

        keystate = pygame.key.get_pressed()
        direct_x = keystate[K_RIGHT] - keystate[K_LEFT]
        direct_y = keystate[K_DOWN] - keystate[K_UP]
        game_obj.move(direct_x, direct_y)

        #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
