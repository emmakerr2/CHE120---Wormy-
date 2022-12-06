# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

#This line is importing the pygame, random and sys modules - BC
import random, pygame, sys

#This line is importing the pygame functions from the module - BC
from pygame.locals import *

pygame.mixer.init()
pygame.mixer.music.load("garage.mp3") 
pygame.mixer.music.play(-1,0.0)

#This line is setting the frames per second. It denotes how smoothly the game will run - BC
#This line sets the speed that any animated objects will move at - VG
#EDIT: changed the FPS from 15 to 10 to make game slower
FPS = 10

#WINDOWWIDTH is the width of the grid players play wormy on that appears on their console when wormy is run - BC
#WINDOWHEIGHT is the height of the grid players play wormy on that appears on their console when wormy is run - BC
#CELLSIZE is the size of the cells in the grid.  - BC
#EDIT: changed window dimensions to be a larger window
WINDOWWIDTH = 1000
WINDOWHEIGHT = 600

#EDIT: changed the cellsize from 20 to 25 to make larger squares
CELLSIZE = 25

#Theese assertion statements makes sure only a whole number of cells can fit in the window. Here it is referring to the amount of cells that can fit across - BC
#If the window width or height is not a multiple of the cellsize, program encounters an assertion error - VG
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."

#This line makes sure that the amount of cells that fit horizontally/vertically is an integer - BC
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#     R    G    B
#The above comment indicates that RGB is used to initialize certain colours to create colour shades - BC

#The colour white has 255 of red, green, and blue so this line sets the colour white - BC
WHITE     = (255, 255, 255)
#The colour black has 0 of red, green, and blue so this line sets the colour black  - BC
BLACK     = (  0,   0,   0)
#The colour red has 255 of red, so this line sets the colour red  - BC
RED       = (255,   0,   0)
#The colour green has 255 of green, so this line sets the colour green - BC
GREEN     = (  0, 255,   0)
#The colour dark green has 155 of green, so this line sets the colour dark green - BC
DARKGREEN = (  0, 155,   0)
#The colour dark gray has 40 of red, green, and blue so this line sets the colour dark gray - BC
DARKGRAY  = ( 40,  40,  40)
ORANGE    = (255, 127, 0)
PINK      = (255, 0, 212)
LIGHTPINK = (255, 102, 255)
#BGCOLOR stands for background colour, this is setting the background colour to black - BC
BGCOLOR = BLACK

##Defining and initializing these variables here makes them global variables that can be used throughout the entire .py file - VG

#UP is defined as the string up - BC
UP = 'up'
#DOWN is defined as the string down.  - BC
DOWN = 'down'
#LEFT is defined as the string left. - BC
LEFT = 'left'
#RIGHT is defined as the string right.  - BC
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    #global variables will be accessible anywhere in the program, these won't need to be re-initialized - VG

    #initializes the pygame modules - VG
    pygame.init()
    
    #creates a clock object that is used to keep track of time, and has the ability to track the frames per second, and attaching it to the variable FPSCLOCK - EK
    FPSCLOCK = pygame.time.Clock()
    #setting DISPLAYSURF as function used to set the display mode to a specific width and height - EK
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    #sets the game’s font to a font imported into the game from a text file in the size 18 - EK
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    #if the display’s window has a caption at the top, this will display it as wormy, showing users the game they will be playing - EK
    pygame.display.set_caption('Wormy')

    #displays the start screen, that shows the name of the game and prompts users to press a key to begin playing, the inputs for this come from a function that is defined later in the code - EK
    showStartScreen()

    #logic set to always be True, while loop repeats indefinitely - VG
    while True:
        runGame()
        #calls the runGame function - VG
        showGameOverScreen()
        #calls the game over screen function once the runGame function completed - VG


def runGame():
    # Set a random start point.
    #generates a random integer value for the starting position of the worm on the x axis - EK
    startx = random.randint(5, CELLWIDTH - 6)
    #generates a random integer value for the starting position of the worm on the y axis - EK
    starty = random.randint(5, CELLHEIGHT - 6)

    #sets the starting coordinates of the worm to that of the random integer values determined above - EK
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    
    #has the worm travel right in regards to its starting position, and the worm can only move in the rightwards direction - EK
    #user input can switch the direction later, this is the inital direction from start point - VG
    direction = RIGHT

    #generates an apple in a randomly selected location somewhere within the grid - EK
    apple = getRandomLocation()
    orange = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): #event handling loop
            if event.type == QUIT:
                
                #if the game has ended at the startup screen, and the user has quit, the game will terminate and close down - EK
                terminate()

            #at the startup screen, the game prompts users to press down a key, this essentially commands the game itself to open and allows users to play - EK
            #if the user presses down a key rather than quits the game, the program responds by generating more commands to allow a playable program - EK
            elif event.type == KEYDOWN:

                #These selected keys and/or arrows on the user’s keyboard output different directions within the game - EK
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN

                #if the escape key has been hit, it urges the game to close - EK
                elif event.key == K_ESCAPE:
                    terminate()

        #Check if the worm has hit itself or the edge
        #if either x or y coordinate of the worm's head is equal to a coordinate outside the window width or height - VG
        #Edit: Instead of dying when you hit the edges of the window, you come out the other side (ei. pacman)
        for i in range(len(wormCoords)):
            if wormCoords[i]['x'] <= -1:
                wormCoords[i]['x'] = CELLWIDTH + i
                pygame.time.wait(100)
                
            elif wormCoords[i]['x'] >= CELLWIDTH:
                wormCoords[i]['x'] = -1 - i
                pygame.time.wait(100)
                
            elif wormCoords[i]['y'] <= -1:
                wormCoords[i]['y'] = CELLHEIGHT+ i
                pygame.time.wait(100)
                
            elif wormCoords[i]['y'] >= CELLHEIGHT:
                wormCoords[i]['y'] = -1 - i
                pygame.time.wait(100)

        #checking to see if the worm’s position has changed to where it is hitting the end of the grid or the “wall”, and if it has collided with itself which triggers the end of the game - EK
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over
            
        if (len(wormCoords) <= 2):
            return
            
        if wormCoords[HEAD]['x'] == orange['x'] and wormCoords[HEAD]['y'] == orange['y']:
            del wormCoords[-1]
            orange = getRandomLocation()

        # check if worm has eaten an apply by comparing the worm's head position and the apple's position - VG
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment

            #checks to see if the worm’s head is in the same location (for both the x and y direction) as the apple, and then if the apple has been consumed a new one will be generated in a random location - EK
            apple = getRandomLocation() # set a new apple somewhere
            orange = getRandomLocation()
        else:
             #otherwise remove worm's tail segment by one unit of the grid - EK
            del wormCoords[-1] # remove worm's tail segment

        #moves the worm by adding certain segments to the head depending on the position the worm is being moved in, ex. if the direction is up it moves -1 in the y direction - EK
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)

        #fills background with the chosen background colour, and draws the gridlines - VG
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        
        #This will generate the images of the worm at the given coordinates, the apple, and the score of the game, which is given as the worm’s length minus 3 (as this is the starting length of the worm) - EK
        drawWorm(wormCoords)
        drawApple(apple)
        drawOrange(orange)
        
        #EDIT: changed the score to be the length of the worm, representing number of segments
        drawScore(len(wormCoords))

        #updates the display at a rate of 40 frames per second - VG
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, PINK)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

#this function handles any user input by key presses - VG
def checkForKeyPress():
    
    #If a key is not pressed, and the user has prompted the game to quit, it will terminate - EK
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    #creates a queue of key press events to execute - VG
    keyUpEvents = pygame.event.get(KEYUP)

    #if there are no events in the queue, do nothing - VG
    if len(keyUpEvents) == 0:
        return None

    #if the ESC key is pressed while the game is running the game will terminate. - BC
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    #In the start screen, it displays in a given font and size the name of the game, “Wormy!” twice, in two different colours of green - EK
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    
    #initializing the white title to say 'Wormy!' and be white text in a darkgreen textbox - VG
    titleSurf1 = titleFont.render('Wormy!', True, PINK, WHITE)
    #initializing the green title to say 'Wormy!' and be green text in a default transparent textbox - VG
    titleSurf2 = titleFont.render('Wormy!', True, LIGHTPINK)

    #sets the initial orientation of the two title textboxes to be unrotated - VG
    degrees1 = 0
    degrees2 = 0
    
    while True:
        #fill the background with the chosen background colour - VG
        DISPLAYSURF.fill(BGCOLOR)

        #orientate the white text in green box at set number of degrees - VG
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        #setting up the textbox for the white title to be placed in - VG
        rotatedRect1 = rotatedSurf1.get_rect()
        #centre the rectangle in the centre of the window - VG
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        #place the white title in its respective textbox on the DISPLAYSURF - VG
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        #orientate the green text in its textbox at set number of degrees - VG
        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        #setting up the textbox for the green title to be placed in - VG
        rotatedRect2 = rotatedSurf2.get_rect()
        #centre the rectangle in the centre of the window - VG
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        #place the green title in its respective textbox on the DISPLAYSURF - VG
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        #pressing any key breaks this function - the game will start after showing this start screen - VG
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        
        #the display is updated at the chosen FPS rate - VG
        #animating this display updates the degrees at a FPS rate, rotating the two titles - VG
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        #white title rotates 7 degrees around its axis per frame - VG
        degrees1 += 3
        
        #green title rotates 7 degrees around its axis per frame - VG
        degrees2 += 7 

#this function is used when the game is being ended - VG
def terminate():
    #pygame is quit
    pygame.quit()
    #system exits, closing the entire window wormy is played in - VG
    sys.exit()

#generates a random set of coordinates on the grid
def getRandomLocation():
    #uses random module to get a randomized integer between 0 and the
    #objects are drawn based off the cooridnate of their upper left most corner
    #function returns a dictionary that has x and y each equal new randomized coordinates
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

#this function produces the screen appearing after the user crashes into a wall, ending that game
def showGameOverScreen():
    #this line initializes the game over font style and size of the text 
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)

    #renders the text that says game and over
    #True for antialias option ensures that the text will be high definition
    #third parameter says that the text is white
    gameSurf = gameOverFont.render('Game', True, PINK)
    overSurf = gameOverFont.render('Over', True, PINK)

    #these rectangles are the spaces where each word will be written
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()

    #orientates the rectangle 'textboxes' with the centre being window width / 2 (middle of window)
    #'game' textbox is 10 units down from the top of the screen
    #'over' textbox is set to be 25 units below the bottom of the word game
    #midtop indicates that its the centre of the words that are placed at those coordinates
    gameRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 150)
    overRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    #prints each word out onto its respective rectangle on the display interface
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)

    #calls the press key message function to prompt user to restart
    drawPressKeyMsg()

    #calls the function that switches the screen to the surface that has 'game over' displayed
    pygame.display.update()

    #wait for 500 milliseconds before detecting a key press as a restart attempt
    pygame.time.wait(500)

    #Clears out any key presses in the event queue
    checkForKeyPress() 

    #logic set to always be True, while loop repeats indefinitely
    while True:
        if checkForKeyPress():
            #if key is pressed, restart gameplay
            pygame.event.get()
            #return to end the gameover function
            return

def drawScore(score):
    #intializes the score text
    #sets the text to be variable depending on user's current score
    #antialias set to True for smooth text display
    #colour set to white RGB variable
    
    #Changed the score caption to say length, representing the number of segments in the worms
    scoreSurf = BASICFONT.render('Length: %s' % (score), True, PINK)

    #creates the 'textbox' rectangle the score will be placed into
    scoreRect = scoreSurf.get_rect()

    #the top left of the score textbox positioned 120 units away from right edge of screen
    #y coordinate is 10 units down from top of screen
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)

    #places the score text into its textbox on DISPLAYSURF
    DISPLAYSURF.blit(scoreSurf, scoreRect)

#this function continually re-draws the worm as it moves across the screen
#parameter worm coords is a list containing a dictionary for each segment of the worm that exists at a given time
#each dictionary has keys 'x' and 'y' to keep track of these coordinates
#coord['x'] and coord['y'] hold the coordinate values of that particular segment at a given time on the grid
def drawWorm(wormCoords):

    #for loop, iterating over each element in the wormCoords list
    #each coord element is a dictionary
    for coord in wormCoords:
        #takes x key in that segment's dictionary, obtains matching value from dictionary, this is the x coordinate of where that worm segment is drawn
        x = coord['x'] * CELLSIZE
        
        #takes y key in that segment's dictionary, obtains matching value from dictionary, this is the x coordinate of where that worm segment is drawn
        y = coord['y'] * CELLSIZE

        #x and y are multiplied by cellsize so their coordinates match the square of the grid they correspond to, rather than the smaller units within the window

        #pygame.Rect used to initialize the rectangle itself
        #it will have coordinates x and y, and be cellsize by cellsize in shape
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)

        #places each worm segment square onto the displaysurf interface
        #colour of the worm will be dark green
        #wormSegmentRect argument is the pre-initialized shape that is the rectangle being drawn
        pygame.draw.rect(DISPLAYSURF, PINK, wormSegmentRect)

        #these two lines create the same size rectangle, that also has the same coordinates less 4, and 8 units smaller in length and height
        #these rectangles are lighter green, and drawn inside each of the worm's segments
        #each segments coordinates are x+4 and y+4 as the rectangle drawn based off the top left corner's coordinates
        #+4 will allow the inner segment to be centred within the larger dark green segments
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, LIGHTPINK, wormInnerSegmentRect)


#this function places each apple on the grid for worm to collect
#coord is a parameter obtained from the argument "random.location"
#coord is a dictionary of 2 items, 'x' and 'y' each equal to their own randomized value within the windows grid
def drawApple(coord):
    #takes x key in dictionary, obtains value, multiplying by set cellsize, this will be x coordinate of where apple is drawn
    x = coord['x'] * CELLSIZE
    
    #takes x key in dictionary, obtains value, multiplying by set cellsize, this is y coordinate of where apple is drawn
    y = coord['y'] * CELLSIZE

    #x and y are multiplied by cellsize so their coordinates match the square of the grid they correspond to, rather than the pixel within the window
    
    #pygame.Rect used to initialize the shape itself
    #it will have coordinates x and y, and be cellsize by cellsize in shape
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)

    #places the apple shape onto the displaysurf interface
    #colour of the apple will be red
    #appleRect parameter is where the pre-initialized shape is stated to be the rectangle being drawn
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawOrange(coord):
    x = coord['x']*CELLSIZE
    y = coord['y']*CELLSIZE
    orangeRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, ORANGE, orangeRect)

#this function draws the bounds that the worm is able to move within during the game
def drawGrid():

    #this for loop draws the vertical gridlines
    #takes the entire width of the space and stops at every cellsize number of pixels to draw line
    #cellsize is a defined variable, initialized to be 20 units in width
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        
        #pygame.draw.line command adds a straight, line on the displaysurf surface
        #colour chosen in darkgray, already defined (R,G,B) values
        #start position is (x,y) = (x,0), or the uppermost left corner of the window 
        #each line is drawn from top to bottom of the window
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
        
        #this for loop draws the horizontal grid lines
        #takes the entire height of the space and stops at every cellsize number of pixels to draw a line
        #cellsize is a defined global variable, initialized to be 20 units
        
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        
        #pygame.draw.line command adds a straight, line on the displaysurf surface
        #lines chosen to be darkgray, from an already named variable
        #start position is (x,y) = (0,y) or the uppermost left corner of the window
        #each line is drawn from left to right side of the window
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

    #these two for loops create the grey squares that the worm travels within
    #given that both horizontal and vertical lines are drawn over the same interval (cellsize) these boxes are square


if __name__ == '__main__':
    #main function, using a magic or dunder method automatically run
    #calling main() function starts the program
    main()
