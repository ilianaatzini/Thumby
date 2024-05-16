import time
import thumby
import math

'''
TODO:
- Only draw GameElements currently visible on the screen
- Walking animation
'''

CAT_JUMP_HEIGHT = 20
CAT_FLOOR = 31

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)

gameElements = {}

class Rect():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class GameImage:
    def __init__(self, imgMap, width, height, imgMaskMap = None):
        self.imgMap = imgMap
        self.width = width
        self.height = height
        self.imgMaskMap = imgMaskMap

class Direction:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class Cat:
    def __init__ (self):
        self.xPos = 0
        self.yPos = CAT_FLOOR
        self.imageXPos = 15
        self.facingDirection = Direction.RIGHT
        self.remainingJump = 0
        self.feetOnSurface = True
        self.catStill = GameImage(bytearray([240,232,100,100,96,224,216,112,88,0,1,0,0,0,0,1,0,0]), 9, 9, 
                                  bytearray([240,232,100,100,96,224,248,112,120,0,1,0,0,0,0,1,0,0]))
        self.catJump = GameImage(bytearray([48,232,118,48,56,28,59,46,75,1,0,0,0,0,0,0,0,0]),9,9,
                                 bytearray([48,232,118,48,56,28,63,46,79,1,0,0,0,0,0,0,0,0]))
        
    def getImage(self):
        if self.remainingJump > 0:
            return self.catJump
        else:
            return self.catStill

def wouldBeNoCollision(cat:Cat, gameElements, direction:int):
    catRect = None

    if direction == Direction.LEFT:
        catRect = Rect(cat.xPos-1, cat.yPos, cat.catStill.width, cat.catStill.height)
    elif direction == Direction.RIGHT:
        catRect = Rect(cat.xPos+1, cat.yPos, cat.catStill.width, cat.catStill.height)
    elif direction == Direction.UP:
        catRect = Rect(cat.xPos, cat.yPos-1, cat.catStill.width, cat.catStill.height)
    elif direction == Direction.DOWN:
        catRect = Rect(cat.xPos, cat.yPos+1, cat.catStill.width, cat.catStill.height)


    for key, value in gameElements.items():
        for gameElement in value:
            if gameElement.isSolid and rectanglesCollided(catRect, Rect(key, gameElement.y, gameElement.image.width, gameElement.image.height)):
                return False

    return True

def rectanglesCollided(rect1:Rect, rect2:Rect):
    # Calculate the edges of each rectangle
    rect1_left = rect1.x
    rect1_right = rect1.x + rect1.width
    rect1_top = rect1.y
    rect1_bottom = rect1.y + rect1.height
    
    rect2_left = rect2.x
    rect2_right = rect2.x + rect2.width
    rect2_top = rect2.y
    rect2_bottom = rect2.y + rect2.height
    
    # Check for overlap on the x-axis
    if rect1_right > rect2_left and rect1_left < rect2_right:
        # Check for overlap on the y-axis
        if rect1_bottom > rect2_top and rect1_top < rect2_bottom:
            return True
    return False


cat = Cat()
smallGrassImage = GameImage(bytearray([1,6,0,4,2]), 5, 3)
bigGrassImage = GameImage(bytearray([2,12,0,12,3]), 5, 4)
platformImage = GameImage(bytearray([5,1,4,5,1,4,5,1,4,5,1,4,5]), 13, 3)
flowerImage = GameImage(bytearray([16,32,58,37,18]), 5, 6)

class GameElement:
    def __init__(self, y: int, image: GameImage, isSolid: bool):
        self.y = y
        self.image = image
        self.isSolid = isSolid

def populateMap():
    gameElements[30] = [GameElement(34, flowerImage, False)]
    gameElements[40] = [GameElement(37, platformImage, True), GameElement(33, platformImage, True)]
    gameElements[65] = [GameElement(28, platformImage, True)]
    gameElements[90] = [GameElement(25, platformImage, True)]
        
populateMap()

while(1):
    t0 = time.ticks_ms()   # Get time (ms)
    thumby.display.fill(0) # Fill canvas to black

    if thumby.buttonL.pressed():
        cat.facingDirection = Direction.LEFT
        if cat.xPos > 1:
            if wouldBeNoCollision(cat, gameElements, Direction.LEFT):
                cat.xPos -= 1
        
    if thumby.buttonR.pressed():
        cat.facingDirection = Direction.RIGHT
        if wouldBeNoCollision(cat, gameElements, Direction.RIGHT):
            cat.xPos += 1

    # start jump
    if thumby.buttonA.pressed():
        if cat.feetOnSurface == True:
            cat.remainingJump = CAT_JUMP_HEIGHT
    
    # moving upwards during jump
    if cat.remainingJump > 0:
        if wouldBeNoCollision(cat, gameElements, Direction.UP):
            # there's nothing above and we can keep moving upwards
            cat.yPos -= 1
            cat.remainingJump -= 1
            cat.feetOnSurface = False
        else:
            # we collided so stop jumping
            cat.remainingJump = 0

    
    # check the cat could fall downwards so long as we aren't currently jumping upwards
    if cat.yPos < CAT_FLOOR and cat.remainingJump <= 0:
        if wouldBeNoCollision(cat, gameElements, Direction.DOWN):
            # move downwards
            cat.yPos +=1
            if (cat.yPos >= CAT_FLOOR):
                # we landed on the floor
                cat.feetOnSurface = True
        else:
            # we landed on some surface
            cat.feetOnSurface = True

    for key, value in gameElements.items():
        for gameElement in value:
            thumby.display.blit(gameElement.image.imgMap, (key-cat.xPos)+cat.imageXPos, gameElement.y, gameElement.image.width, gameElement.image.height, -1, 0, 0)
    
    # Display the bitmap using bitmap data, position, and bitmap dimensions
    thumby.display.blitWithMask(cat.getImage().imgMap, cat.imageXPos, cat.yPos, cat.getImage().width, cat.getImage().height, -1, cat.facingDirection, 0, cat.getImage().imgMaskMap)
    thumby.display.update()