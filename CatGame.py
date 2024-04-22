import time
import thumby
import math

catmap = bytearray([240,232,100,100,96,224,216,112,88,
           0,1,0,0,0,0,1,0,0])

# Make a sprite object using bytearray (a path to binary file from 'IMPORT SPRITE' is also valid)
catSprite = thumby.Sprite(9, 9, catmap)

catSprite.x = 35
catSprite.y = 19

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)

while(1):
    t0 = time.ticks_ms()   # Get time (ms)
    thumby.display.fill(0) # Fill canvas to black

    if thumby.buttonL.pressed():
        catSprite.x -= 1
        
    if thumby.buttonR.pressed():
        catSprite.x += 1

    # Display the bitmap using bitmap data, position, and bitmap dimensions
    thumby.display.drawSprite(catSprite)
    thumby.display.update()

def populateMap():
    sprites = {}
    sprites[30] = [thumby.Sprite(9, 9, catmap)]

    for key, value in sprites.items():
        print(key, " -> ", value)