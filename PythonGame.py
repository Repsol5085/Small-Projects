#Snake Game
import time, sys, random
import pygame

checkforerror = pygame.init()

if checkforerror[1] > 0:
    print("(!) ERROR {0} initializing errors".format(checkforerror[1]))
    sys.exit(-1)
else:
    print("(+) Pygame initialized!")

#Game windows (surface)
#using pygame
playSurface = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Python Game')
#Colors for the game rgb
blue = pygame.Color(0, 110, 255)#Snake
red = pygame.Color(226, 48, 25)#Game Over
textColor = pygame.Color(219, 208, 207)# Other Text WHITE-ISH COLOR
bgColor = pygame.Color(36, 43, 44)#Background DARK GRAY
foodyellow = pygame.Color(255, 211, 16)#Food

#FPS Control
fpsController = pygame.time.Clock()

#Positions
snakePos = [150, 100]
snakeBody = [[150, 100], [140, 100], [130, 100]]
snakeBodyBackup = snakeBody
foodPos = [random.randrange(1, 128)*10, random.randrange(1, 72)*10]
foodSpawn = True

#Vars
direction = 'RIGHT' #direction headed
changeto = direction #change direction
score = 0 #current score
difficulty = -1 #difficulty level
started = False # has the game been started
paused = False  # has the game been paused
ended = False   # has there been an "Game Over" screen 

#exiting the game 
def exitGame():
    pygame.quit()
    sys.exit()
   
#gameover
def gameOver():
    fontt = pygame.font.SysFont('courier', 100) #game over font 
    gOSurf = fontt.render('Game Over!', True, red)  #game over surface render
    gORect = gOSurf.get_rect()  
    gORect.midtop = (640, 40)   #position
    playSurface.blit(gOSurf, gORect) 
    retryfont = pygame.font.SysFont('courier', 40)  #retry font
    retrySurf = retryfont.render('Retry? r=Retry; q=Quit;', True, textColor)
    retryRect = retrySurf.get_rect()
    retryRect.midtop = (640, 300)
    playSurface.blit(retrySurf, retryRect)
    showScore(0) #score text change on game over screen
    global ended 
    ended = True
    pygame.display.flip()

#score changer
def showScore(go=1):
    sfont = pygame.font.SysFont('courier', 25)  #score font/text/position/render
    sSurf = sfont.render('Score: {0}'.format(score), True, textColor)
    sRect = sSurf.get_rect()
    if go == 1:
        sRect.midtop = (80, 20)     #not on Game Over Screen
    else:
        sRect.midtop = (640, 200)   #on Game Over Screen
    playSurface.blit(sSurf, sRect)

#restarting the game returing most things to original states
def restart():  
    global ended 
    ended = False
    global started
    started = True
    global score 
    score = 0
    global paused
    paused = False
    global snakeBody 
    snakeBody = [[150, 100], [140, 100], [130, 100]]
    global snakePos 
    snakePos[0]=150
    snakePos[1]=100
    global direction
    direction = 'RIGHT'
    global changeto 
    changeto = direction

#pause screen
def pausedGame():
    pauseFont = pygame.font.SysFont('courier',100)  
    pauseSurf = pauseFont.render('PAUSED',True,textColor)
    pauseRect = pauseSurf.get_rect()
    pauseRect.midtop = (640, 20)
    sfont = pygame.font.SysFont('courier', 50)
    sSurf = sfont.render('Score: {0}'.format(score), True, textColor)
    sRect = sSurf.get_rect()
    sRect.midtop = (640, 200)
    retryfont = pygame.font.SysFont('courier', 40)
    retrySurf = retryfont.render("Restart? r=Restart; q=Quit;", True, textColor)#Change difficulty: 1=EASY; 2=MEDIUM;
    retryRect = retrySurf.get_rect()
    retryRect.midtop = (640, 300)
    cdfont = pygame.font.SysFont('courier', 40)
    cdSurf = cdfont.render("Change difficulty: 1=EASY; 2=MED; 3=HARD", True, textColor)
    cdRect = cdSurf.get_rect()
    cdRect.midtop = (640, 400)
    playSurface.blit(pauseSurf,pauseRect)
    playSurface.blit(sSurf,sRect)
    playSurface.blit(retrySurf,retryRect)
    playSurface.blit(cdSurf,cdRect)

#start menu of the game
def startmenu(running=False):
    if running == False:
        startFont = pygame.font.SysFont('courier',100)
        startSurf = startFont.render('THE PYTHON GAME',True,textColor)
        startRect = startSurf.get_rect()
        startRect.midtop = (640, 20)
        diffiFont = pygame.font.SysFont('courier',40)
        diffiSurf = diffiFont.render('Chose difficulty : 1=EASY; 2=MED; 3=HARD;',True, textColor)
        diffiRect = diffiSurf.get_rect()
        diffiRect.midtop = (640, 200)
        coolfont = pygame.font.SysFont('courier', 18)
        coolSurf = coolfont.render('"Adding some text down here to make it look cool..." - Repsol5085', True, textColor)
        coolRect = coolSurf.get_rect()
        coolRect.midtop = (640, 680)
        playSurface.blit(coolSurf,coolRect)
        playSurface.blit(startSurf,startRect)
        playSurface.blit(diffiSurf,diffiRect)
        pygame.display.flip()
    
#easy mode
def easyMode():
    if snakePos[0]>1270 :
        snakePos[0]=0
    if snakePos[0]<0:
        snakePos[0]=1270
    if snakePos[1]>710:
        snakePos[1]=0
    if snakePos[1]<0:
        snakePos[1]=710

#hard mode
def medMode():
    if snakePos[0]>1270 or snakePos[0] < 0:
        gameOver()
    if snakePos[1]>710 or snakePos[1] <0:
        gameOver()

#difficulty Selector
def difficultySel(diff):
    if diff == 0:
        easyMode()
    elif diff == 1 or diff == 2:
        medMode()   
    
#Logic 
#loops and frames
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()
        elif event.type == pygame.KEYDOWN:
            if paused == True:                #if game has been paused
                if event.key == pygame.K_q:
                    exitGame()
                if event.key == pygame.K_r:
                    restart()
                if event.key == pygame.K_1:
                    difficulty = 0
                    paused = False
                if event.key == pygame.K_2:
                    difficulty = 1
                    paused = False
                if event.key == pygame.K_3:
                    difficulty = 2
                    paused = False
                if event.key == pygame.K_ESCAPE:
                    paused=False
            elif ended == True:             #if game over     
                if event.key == pygame.K_q:
                    exitGame()
                if event.key == pygame.K_r:
                    restart()
            elif started==True and ended == False:  #has been started (a difficulty has been sel)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    changeto = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    changeto = 'LEFT'
                if event.key == pygame.K_UP or event.key == ord('w'):
                    changeto = 'UP'
                if event.key == pygame.K_DOWN or  event.key == ord('s'):
                    changeto = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    paused=True
            else:               #if we haven't selected diff yet
                startmenu()
                if event.key == pygame.K_1:
                    difficulty = 0
                if event.key == pygame.K_2:
                    difficulty = 1
                if event.key == pygame.K_3:
                    difficulty = 2
                if difficulty > -1 :started = True
    
    #checking and changing dir
    if  started==True and ended==False and paused == False:
        if changeto == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'
        if changeto == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'
        if changeto == 'UP' and not direction == 'DOWN':
            direction = 'UP'
        if changeto == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'

        #movement
        if direction == 'RIGHT':
            snakePos[0] += 10
        if direction == 'LEFT':
            snakePos[0] -= 10
        if direction == 'UP':
            snakePos[1] -= 10
        if direction == 'DOWN':
            snakePos[1] += 10

        #snake body movement
        #works by adding and poping an el to
        # the list that is the snake
        snakeBody.insert(0, list(snakePos))
        if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
            timer = time.time() #when we eat the food
            score += 1
            foodSpawn = False
        else:
            snakeBody.pop() #when we don't

        if foodSpawn == False: #spawning food at a random position
            foodPos = [random.randrange(1, 128)*10, random.randrange(1, 72)*10]
        foodSpawn = True

    #setting bg
    playSurface.fill(bgColor)
    for pos in snakeBody: #adding the snake 
        pygame.draw.rect(playSurface,blue,pygame.Rect(pos[0],pos[1],10,10))
    pygame.draw.rect(playSurface,foodyellow,
    pygame.Rect(foodPos[0],foodPos[1],10,10))#adding the food
    difficultySel(difficulty) #cheking diff for collision with self and walls
    #end/pause/start screens 
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()
    if started == True and ended == True:
        gameOver()
    elif paused == True:
        pausedGame()
    else:
        startmenu(started)
    if ended == False and paused == False and started == True:
        showScore()
    pygame.display.flip()
    if difficulty == 2:#hard diff is medium with speed x4
        fpsController.tick(100) #so more fps
    else :
        fpsController.tick(25) 