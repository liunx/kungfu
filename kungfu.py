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

SCREENRECT      = Rect(0, 0, 800, 600)

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

# initializer for class Player
def object_init():
    # init sound
    Player.punch = load_sound('punch.wav')
    """ the single image as default """
    Player.single_image = load_image('stand-still.png')
    Player.image_dict['default'] = load_images('stand-still.png')
    Player.image_dict['left-fist'] = load_images('left-fist.png')
    Player.image_dict['right-fist'] = load_images('right-fist.png')
    Player.image_dict['left-kick'] = load_images('left-kick.png')
    Player.image_dict['right-kick'] = load_images('right-kick.png')
    Player.action_dict[K_a] = '-fist'
    Player.action_dict[K_s] = '-kick'


#classes for our game objects
class Player(pygame.sprite.Sprite):
    speed = 1
    animcycle = 12
    delay = 20
    images = []
    single_image = None
    image_dict = {}
    action_dict = {}
    punch = None
    """ add a new sprite """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.image = self.single_image
        self.images.append(self.single_image)
        # posite player on the midbotton
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.frame = 0
        self.images_len = 1
        # we just can complete one action before doing a new action
        self.do_action = 0
        self.delta_frame = 0
        self.direct_x = 0
        self.direct_y = 0
        self.curr_key = None

    def update(self):
        """ show our sprite up """
        if self.do_action == 0:
            self.image = self.image_dict['default'][0]
            self.frame = 0
        else:
            self.frame = self.frame + 1
            image_index = self.frame // self.animcycle % len(self.images)
            # check delay
            if image_index == (len(self.images) - 1) and self.delta_frame == self.delay:
                self.do_action = 0
                self.delta_frame = 0
            else:
                self.delta_frame = self.delta_frame + 1
            self.image = self.images[image_index]

    def move(self, direct_x, direct_y):
        """ move the player """
        self.rect.move_ip((direct_x  - self.direct_x) * self.speed, (direct_y - self.direct_y) * self.speed);
        self.direct_x = direct_x
        self.direct_y = direct_y

    def get_key(self, key):
        """ get user input and reponse in actions """
        if self.do_action == 1:
            return

        if key in self.action_dict:
            self.curr_key = self.action_dict[key]
        else:
            button = None
            if key == 'LEFT':
                button = 'left'
            elif key == 'MIDDLE':
                button = 'middle'
            elif key == 'RIGHT':
                button = 'right'
            else:
                print("Unknown mouse button pressed!")
                return
            if self.curr_key is not None:
                self.images = []
                key = button + self.curr_key
                if key in self.image_dict:
                    self.images = self.image_dict[key]
                    self.do_action = 1
                    self.punch.play()

#classes for our game objects
class Mouse(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = load_image('mouse-target.png')
        self.rect = self.image.get_rect()

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

# These classes used collison
class Attack(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, image):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
        self.image = load_image(image)
        self.rect = self.image.get_rect()

    def update(self):
        pass

class Defend(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, image):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
        self.image = load_image(image)
        self.rect = self.image.get_rect()
    
    def update(self):
        pass


class Score(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, image):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
        self.image = load_image(image)
        self.rect = self.image.get_rect()
    
    def update(self):
        pass

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    pygame.display.set_caption('Kung Fu')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    object_init()
    game_obj = Player()
    mouse = Mouse()
    allsprites = pygame.sprite.RenderPlain((game_obj, mouse))

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
            elif event.type == MOUSEBUTTONDOWN:
                # attacking when mouse down
                key = None
                button1, button2, button3 = pygame.mouse.get_pressed()
                # we don't allow both buttons pressed now
                if button1 == 1:
                    key = 'LEFT'
                elif button2 == 1:
                    key = 'MIDDLE'
                elif button3 == 1:
                    key = 'RIGHT'
                game_obj.get_key(key)

        allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
