import pygame
from pygame.locals import *
import math
import string
import random
import external

#written with a lot of help from the docs https://www.pygame.org/docs

################################################################################
# DATA STRUCTS
################################################################################

#external.transparentify(data.personImage, 80)

class Cell(object):
    def __init__(self):
        self.items = []

    def addItem(self, item):
        self.items.append(item)

    def containsInstance(self, data, cls):
        for item in self.items:
            if type(item) == cls:
                return True
        return False

class Data(object):
    pass

class GameObject(pygame.sprite.Sprite):
    def __init__(self, data, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = x, y
        self.data = data
        self.image = data.emptyImage
        self.rect = self.image.get_rect()

    def updateSelf(self, data):
        self.updatePosition(data)

    def updatePosition(self, data):
        width, height = self.rect[2], self.rect[3]
        screenX, screenY = gridToScreen(data, self.x, self.y)
        self.rect.center = (screenX + width//2, screenY + height//2)

class Empty(GameObject):
    def __init__(self, data, x, y):
        super().__init__(data, x, y)
        self.image = data.emptyImage
        self.rect = self.image.get_rect()

class Road(GameObject):
    def __init__(self, data, x, y):
        super().__init__(data, x, y)
        self.image = data.roadImage
        self.rect = self.image.get_rect()

class Person(GameObject):
    def __init__(self, data, x, y, name, hunger, sleepiness):
        super().__init__(data, x, y)
        self.name = name
        self.hunger = hunger
        self.sleepiness = sleepiness
        self.moveSpeed = 5
        self.image = data.personImage
        self.rect = self.image.get_rect()
        self.updatePosition(data)

    def updatePosition(self, data):
        width, height = self.rect[2], self.rect[3]
        screenX, screenY = gridToScreen(data, self.x, self.y)
        self.rect.center = (screenX + width//2, screenY)

    def move(self, direction):
        self.x += direction[0]
        self.y += direction[1]

################################################################################
# IMPLEMENT DATA STRUCTS
################################################################################

def newRoad(data, row, col): #x and y in gridX and gridY
    if not data.grid[row][col].containsInstance(data, Road):
        road = Road(data, col, row)
        data.grid[row][col].addItem(road)
        data.roads.add(road)
        print(road.x, road.y)
    else:
        print("sorry, a Road is already there")

def newPerson(data, row, col): #x and y in gridX and gridY
    if not data.grid[row][col].containsInstance(data, Person):
        name = random.choice(tuple(data.firstNames)) + " "\
                + random.choice(string.ascii_uppercase)
        person = Person(data, col, row, name,100,100)
        data.grid[row][col].addItem(person)
        data.people.add(person)
        print(person.name)
    else:
        print("sorry, a Person is already there")

def updateAndAdd(data):
    #update sprites
    for empty in data.empties:
        empty.updateSelf(data)
    for road in data.roads:
        road.updateSelf(data)
    for person in data.people:
        person.updateSelf(data)

    #update groups
    # data.empties.update()
    # data.people.update()

    #draw on screen
    data.empties.draw(data.screen) #least recent call goes to back of canvas
    data.roads.draw(data.screen)
    data.people.draw(data.screen)

################################################################################
# UTILITY
################################################################################

#converts an x, y coord to its scrollX, scrollY, coordinates. returns tuple

def validGridPos(data, gridRow, gridCol):
    return gridRow >= 0 and gridRow < len(data.grid)\
        and gridCol >= 0 and gridCol < len(data.grid[0])

def gridToScreen(data, x, y):
    return (x * data.gridPxLen + data.scrollX,
            y * data.gridPxLen + data.scrollY)

#converts an x, y coord on screen to value in the grid array
def screenToGrid(data, x, y):
    return ((x - data.scrollX)// data.gridPxLen,
            (y - data.scrollY)// data.gridPxLen)



################################################################################
# EVENT HANDLING
################################################################################

def eventHandler(event, data):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mousex = pygame.mouse.get_pos()[0]
        mousey = pygame.mouse.get_pos()[1]
        col, row = screenToGrid(data, mousex, mousey)
        if validGridPos(data, row, col):
            if data.selection == "Person":
                newPerson(data, row, col)
            if data.selection == "Road":
                newRoad(data, row, col)
        else: print("invalid location (row, col):", row, col)


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
        print("selected person!")
    elif keysPressed[pygame.K_r] == 1:
        data.selection = "Road"
        print("selected road!")

def timerFired(data):
    arrowKeysMovement(data)
    if data.bgMusicChannel.get_queue() ==  None:
        data.bgMusicChannel.queue(data.bgMusic)
        print(data.bgMusicChannel.get_queue())
    updateAndAdd(data)


################################################################################
# GRAPHICS
################################################################################

# def drawImages(data, row, col):
#     x, y = gridToScreen(data, col, row)
#     image = None
#     if type(data.grid[row][col]) == Person:
#         image = data.personImage
#     if image != None:
#         data.screen.blit(image, (x, y))

################################################################################
# INIT
################################################################################

def init(data):
    #screen vars
    data.width, data.height = 900, 800

    #states
    data.selection = None

    copiedInit(data)

    #load music and sounds
    data.playMusic = True #if you should play music
    data.bgMusic = data.mixer.Sound("res/Sounds/1241.ogg")
    data.bgMusicChannel = data.mixer.Channel(0)
    data.bgMusicChannel.play(data.bgMusic)

    #load imgs
    data.emptyImage = pygame.image.load("res/Images/empty.png").convert()
    data.personImage = pygame.image.load("res/Images/person.png").convert_alpha()
    data.restaurantImage = pygame.image.load("res/Images/restaurant.png").convert()
    data.roadImage = pygame.image.load("res/Images/road.png").convert()

    #scroll vars
    data.scrollSpeed = 10
    data.scrollX, data.scrollY = 0, 0

    #load data structs
    data.gridWidth, data.gridHeight = 64, 64
    data.gridPxLen = 32
    data.grid = []
    for i in range(data.gridHeight):
        temp = []
        for j in range(data.gridWidth):
            temp.append(Cell())
        data.grid.append(temp)
    data.empties = pygame.sprite.Group()
    for row in range(data.gridHeight):
        for col in range(data.gridWidth):
            empty = Empty(data, col, row)
            data.empties.add(empty)
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
    data.FPS = 30 # frames per second
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
