import pygame
from pygame.locals import *
import math
import string
import random
import external

#written with a lot of help from the docs https://www.pygame.org/docs

#TODO: ADD MIXER FROM EXTERNALCODE


class Data(object):
    pass

class Shadow(pygame.sprite.Sprite):
    def __init__(self, data, cx, cy):
        self.cx = cx
        self.cy = cy
        self.data = data
        self.image = external.transparentify(data.personImage, 80)

class Road(pygame.sprite.Sprite):
    def __init__(self, data, cx, cy, name):
        pygame.sprite.Sprite.__init__(self)
        self.cx = cx
        self.cy = cy
        self.data = data
        self.name = name
        self.image = None

class Building(pygame.sprite.Sprite):
    def __init__(self, data, cx, cy, name):
        pygame.sprite.Sprite.__init__(self)
        self.cx = cx
        self.cy = cy
        self.data = data
        self.name = name
        self.image = None

class Person(pygame.sprite.Sprite):
    def __init__(self, data, cx, cy, name, hunger, sleepiness):
        pygame.sprite.Sprite.__init__(self)
        self.cx = cx
        self.cy = cy
        self.data = data
        self.name = name
        self.hunger = hunger
        self.sleepiness = sleepiness
        self.image = data.personImage
        self.moveSpeed = 5
        self.rect = self.image.get_rect()
        self.updatePosition(data)

    def updateSelf(self, data):
        # self.move((0,1))
        self.updatePosition(data)

    def updatePosition(self, data):
        self.rect.center = (self.cx + data.scrollX, self.cy + data.scrollY)

    def move(self, direction):
        self.cx += self.moveSpeed * direction[0]
        self.cy += self.moveSpeed * direction[1]

def eventHandler(event, data):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mousex = pygame.mouse.get_pos()[0]
        mousey = pygame.mouse.get_pos()[1]
        newPerson(data, mousex, mousey)

def newPerson(data, x, y):
    name = random.choice(tuple(data.firstNames)) + " "\
            + random.choice(string.ascii_uppercase)
    person = Person(data, x - data.scrollX, y - data.scrollY,
                    name,100,100)
    data.people.add(person)
    print(person.name)

def newRoad(data, x, y):
    road = Road(data, x - data.scrollX, y - data.scrollY)
    data.people.add(person)
    print(person.name)

def arrowKeysMovement(data):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[pygame.K_RIGHT] == 1:
        data.scrollX -= data.scrollSpeed
    elif keysPressed[pygame.K_LEFT] == 1:
        data.scrollX += data.scrollSpeed
    if keysPressed[pygame.K_UP] == 1:
        data.scrollY += data.scrollSpeed
    elif keysPressed[pygame.K_DOWN] == 1:
        data.scrollY -= data.scrollSpeed
    elif keysPressed[pygame.K_p] == 1:
        data.selection = "Person"
    elif keysPressed[pygame.K_b] == 1:
        data.selection = "Building"

def timerFired(data):
    arrowKeysMovement(data)
    if data.bgMusicChannel.get_queue() ==  None:
        data.bgMusicChannel.queue(data.bgMusic)
        print(data.bgMusicChannel.get_queue())
    data.people.update()
    data.people.draw(data.screen)
    for person in data.people:
        person.updateSelf(data)

def init(data):
    #screen vars
    data.width, data.height = 800, 700
    data.cityWidth, data.cityHeight = 25, 25

    #states
    data.selection = None

    copiedInit(data)

    #load music and sounds
    data.playMusic = True #if you should play music
    data.bgMusic = data.mixer.Sound("res/Sounds/1241.ogg")
    data.bgMusicChannel = data.mixer.Channel(0)
    data.bgMusicChannel.play(data.bgMusic)

    #load imgs
    data.personImage = pygame.image.load("res/Images/person.png")
    data.restaurantImage = pygame.image.load("res/Images/restaurant.png")
    data.roadImage = pygame.image.load("res/Images/road.png")

    #scroll vars
    data.scrollSpeed = 10
    data.scrollX, data.scrollY = 0, 0

    #load data structs
    data.board = []
    data.people = pygame.sprite.Group()
    data.roads = pygame.sprite.Group()
    data.buildings = pygame.sprite.Group()
    data.text = pygame.sprite.Group()
    data.menu = pygame.sprite.Group()



    data.firstNames = {"Bob", "Joe", "Steve", "John", "Humphrey", "Ben", "Jack",
                  "Mark", "Paul", "Forrest", "James", "Robert", "Nick", "Egg",
                  "Jackson", "Sally", "Jane", "Holly", "Sophie", "Samantha",
                  "Mary", "Julia", "Betty", "Beep", "MacDonald", "Owen",
                  "Jamie", "Lance", "Carter", "Maria", "Lucy", "Anna", "Amelia",
                  "Gerome", "Xavier", "Wyatt", "Eggbert", "Edward", "Ellie",
                  "Matt", "Shrek", "Fiona", "Belle", "Carrey", "Katie", "Max",
                  "Bo", "Keanu", "Eatington", "George", "Carl", "Caroline",
                  "Gordon", "Teddy", "Annie", "Vivienne", "Leah", "Ticho",
                  "Chad", "Thaddeus", "Tom", "Becky"}

#################################################
#   THE FOLLOWING CODE IS NOT (entirely) MINE   #
#   I PUT IT IN THE MAIN FILE BECAUSE           #
#   IT INITIALIZES SOME VARS THAT I NEED FOR    #
#   THE REST OF THE PROJECT                     #
#################################################

#code from here https://pythonprogramming.net/changing-pygame-icon/
def setIcon():

    gameIcon = pygame.image.load('res/Images/icon.png')
    pygame.display.set_icon(gameIcon)

#run() and copiedInit() uses code from here:
#http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
#by Chris Bradford
#(some parts modified by me to fit my project)

def copiedInit(data):
    data.FPS = 60 # frames per second
    # initialize the pygame module
    pygame.init()
    data.mixer = pygame.mixer
    data.mixer.init()  # for sound

    setIcon()

    data.screen = pygame.display.set_mode((data.width, data.height))
    pygame.display.set_caption("Py Sims")
    data.clock = pygame.time.Clock()
    data.running = True

def run(data):
    # Game Loop
    while data.running:
        data.clock.tick(data.FPS)
        data.screen.fill((0,0,0))
        timerFired(data)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                data.running = False

            #call eventHandler function specified in parameters
            eventHandler(event, data)
        pygame.display.flip()

#runs the python app if this is the designated main script
if __name__=="__main__":
    data = Data() #inspired by 112's data struct in the run function
    init(data)
    #run code
    run(data)

#################################################
# END OF COPIED CODE                            #
#################################################
