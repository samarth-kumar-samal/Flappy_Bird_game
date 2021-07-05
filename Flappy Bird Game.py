import random       # For generating the random numbers in the game 
import sys          # We will use sys.exit to exit the game
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
FPS = 32
SCREENWIDTH = 335
SCREENHEIGHT = 510
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))                                                      # Initialize a window or screen for display
GROUNDY = SCREENHEIGHT * 0.8                                                                                       # Sets the ground of the game which is 80% of the screen heigth
GAME_SPRITES = {}                                                                                                  # Stores the images for the game
GAME_SOUNDS = {}                                                                                                   # Stores the sounds for the game
PLAYER = 'C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/bird.png'                # Stores the location of the player of the game
BACKGROUND = 'C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/background.png'      # Stores the location of the background of the game
PIPE = 'C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/pipe.png'                  # Stores the location of the pipes of the game

def welcomeScreen():
    """
    Shows the welcome images on the screen of the game
    """
    # Location of the player
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():                                            # pygame.event.get() tells about the events happening in the window
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user clicks the space key or up key , start the game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))                     # blit() is used to draw one image onto another
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()                                             # This statement is used to change screen from the current screen to the next screen
                FPSCLOCK.tick(FPS)                                                  # This statement ensures that the game fps should be that much and not more than the given fps value

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4                                                       # Velocity with which the player bird moves forwards
    playerVelY = -9                                                     # Velocity with which the player bird moves up or down
    playerMaxVelY = 10                                                  # Maximum Velocity with which the player bird moves up or down 
    playerMinVelY = -8                                                  # Minimum Velocity with which the player bird moves up or down
    playerAccY = 1                                                      # Acceleration with which the player bird moves up or down

    playerFlapAccv = -8                                                 # Velocity of the player bird while flapping
    playerFlapped = False                                               # It is true only when the player bird is flapping


    while True:
        for event in pygame.event.get():                                                            # For the events happening in the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):             # This is used to exit the game immediately
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):               # This is used to flap the player bird in order to play the game and move forward
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)                             # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False                                                                   # If the player is flapping only once then he bird is not moving up     
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # moving pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Adding a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
            
def isCollide(playerx, playery, upperPipes, lowerPipes):                                        # This is used to test for the crash
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe






if __name__ == "__main__":                                                        # Here the game gets started because this will be the main point
    pygame.init()                                                                 # Initialise all the modules of the pygame
    FPSCLOCK = pygame.time.Clock()                                                # It brings the clock to the game which controls the fps of the game
    pygame.display.set_caption('Flappy Bird by SAM')                              # Sets the title of the game window
    GAME_SPRITES['numbers'] = (                                                   # stores the images of the numbers
        pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/0.png').convert_alpha(),   # convert_alpha() optimises the images    
        pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/1.png').convert_alpha(),    
        pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/message.png').convert_alpha()      # shows the message to the game users
    GAME_SPRITES['base'] =pygame.image.load('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/sprites/base.png').convert_alpha()            # shows the base to the game users
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180),                                                                 # It rotates the pipe image and inveted image will be displayed and it will be rotated through 180    
    pygame.image.load(PIPE).convert_alpha()                                                                                                                        # It displays the erect image of the pipes
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('C:/Users/samar/OneDrive/Documents/Python games/Flappy bird game/gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()                                                     # Shows welcome screen to the user until he presses a button
        mainGame()                                                          # This is the main game function 
        print("""
        **********
        
        Thank you so much for playing my game.Have a nice day
        
        **********""")