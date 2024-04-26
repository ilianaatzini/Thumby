import time
import thumby
import math

'''
TODO:
- Make the platform solid
'''

CAT_JUMP_HEIGHT = 20
CAT_FLOOR = 30

           # BITMAP: width: 5, height: 3
smallGrassMap = bytearray([1,6,0,4,2])

            # BITMAP: width: 5, height: 4
bigGrassMap = bytearray([2,12,0,12,3])

# BITMAP: width: 13, height: 3
platformMap = bytearray([5,1,4,5,1,4,5,1,4,5,1,4,5]
)
# BITMAP: width: 5, height: 6
flowerMap = bytearray([16,32,58,37,18])

#catSprite.x = 2
#catSprite.y = 30

catXpos = 0
catYpos = CAT_FLOOR

catImageX = 2

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)

sprites = {}
    
class GameImage:
    def __init__(self, imgMap, width, height, imgMaskMap = None):
        self.imgMap = imgMap
        self.width = width
        self.height = height
        self.imgMaskMap = imgMaskMap

class Direction:
    RIGHT = 0
    LEFT = 1

class Cat:
    def __init__ (self):
        self.facingDirection = Direction.RIGHT
        self.jumping = 0
        self.catStill = GameImage(bytearray([240,232,100,100,96,224,216,112,88,0,1,0,0,0,0,1,0,0]), 9, 9, 
                                  bytearray([240,232,100,100,96,224,248,112,120,0,1,0,0,0,0,1,0,0]))
        self.catJump = GameImage(bytearray([48,232,118,48,56,28,59,46,75,1,0,0,0,0,0,0,0,0]),9,9,
                                 bytearray([48,232,118,48,56,28,63,46,79,1,0,0,0,0,0,0,0,0]))
        
    def getImage(self):
        if self.jumping > 0:
            return self.catJump
        else:
            return self.catStill

cat = Cat()

smallGrassImage = GameImage(smallGrassMap, 5, 3)
bigGrassImage = GameImage(bigGrassMap, 5, 4)
platformImage = GameImage(platformMap, 13, 3)
flowerImage = GameImage(flowerMap, 5, 6)

class GameElement:
    def __init__(self, y: int, image: GameImage):
        self.y = y
        self.image = image

def populateMap():
    sprites[30] = [GameElement(33, flowerImage)]
    sprites[40] = [GameElement(20, platformImage)]
    sprites[60] = [GameElement(10, platformImage)]
        
populateMap()

while(1):
    t0 = time.ticks_ms()   # Get time (ms)
    thumby.display.fill(0) # Fill canvas to black

    if thumby.buttonL.pressed():
        cat.facingDirection = Direction.LEFT
        if catXpos > 1:
            catXpos -= 1
        
    if thumby.buttonR.pressed():
        cat.facingDirection = Direction.RIGHT
        catXpos += 1
        
    if thumby.buttonA.pressed():
        if cat.jumping <= 0 and catYpos == CAT_FLOOR:
            cat.jumping = CAT_JUMP_HEIGHT
    
    if cat.jumping > 0:
        catYpos -= 1
        cat.jumping -= 1
    elif catYpos < CAT_FLOOR:
        catYpos +=1

    for key, value in sprites.items():
        for gameElement in value:
            thumby.display.blit(gameElement.image.imgMap, key-catXpos, gameElement.y, gameElement.image.width, gameElement.image.height, -1, 0, 0)
    
    # Display the bitmap using bitmap data, position, and bitmap dimensions
    # thumby.display.drawSprite(catSprite)
    thumby.display.blitWithMask(cat.getImage().imgMap, catImageX, catYpos, cat.getImage().width, cat.getImage().height, -1, cat.facingDirection, 0, cat.getImage().imgMaskMap)
    thumby.display.update()