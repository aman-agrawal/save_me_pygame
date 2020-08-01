import pygame,time
from pygame.locals import * # Basic pygame imports
import random
import os
import sys # We will use sys.exit to exit the program

pygame.mixer.init()

pygame.init()
prevtime=time.time()

score = 0

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
screen_width = 900
screen_height = 600
SCREEN = pygame.display.set_mode((screen_width, screen_height))

#Background Image
bgimg = pygame.image.load("bg.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

#Other Images
arrow = pygame.image.load('arrow.png').convert_alpha()
apple = pygame.image.load('apple.png').convert_alpha()
banana = pygame.image.load('banana.png').convert_alpha()
bomb = pygame.image.load('bomb.png').convert_alpha()
cactus = pygame.image.load('cactus.png').convert_alpha()
man = pygame.image.load('man.png').convert_alpha()

#Images Heights
bombh = bomb.get_height()
arrowh = arrow.get_height()
bananah = banana.get_height()
cactush = cactus.get_height()
appleh = apple.get_height()
manh = man.get_height()

#Images Widths
bombw = bomb.get_width()
arroww = arrow.get_width()
bananaw = banana.get_width()
cactusw = cactus.get_width()
applew = apple.get_width()
manw = man.get_width()

manx = 0
many = int(screen_height/2)


# Game sounds
die = pygame.mixer.Sound('audio/die.wav')
hit = pygame.mixer.Sound('audio/hit.wav')
point = pygame.mixer.Sound('audio/point.wav')
swoosh = pygame.mixer.Sound('audio/swoosh.wav')
wing = pygame.mixer.Sound('audio/wing.wav')



# Game Title
pygame.display.set_caption("Save Aman")
pygame.display.update()
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    SCREEN.blit(screen_text, [x,y])

def update_score(applex,appley,bananax,bananay):
	global score

	for x,y in zip(applex,appley):
		if manx+manw/2<=x+applew/2<=manx+manw/2+4 and many<=y<=many+manh :
			score+=1
			point.play()

	for x,y in zip(bananax,bananay):
		if manx+manw/2<=x+bananaw/2<=manx+manw/2+10 and many<=y<=many+manh :
			score+=1
			point.play()

def collide(arrowx,arrowy,bombx,bomby,cactusx,cactusy):
	for x,y in zip(arrowx,arrowy):
		if manx+manw-4<=x+50<=manx+manw and many<=y+170<=many+manh :
			return True

	for x,y in zip(bombx,bomby):
		if manx+manw-4<=x<=manx+manw and many<=y<=many+manh :
			return True

	for x,y in zip(cactusx,cactusy):
		if manx+manw-4<=x<=manx+manw and many<=y<=many+manh :
			return True

	return False


def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    global score 
    score = 0

    global manx,many,prevtime

    speed = 6
    vy = 0

    bombx=[]
    bomby=[]
    applex=[]
    appley=[]
    arrowx=[]
    arrowy=[]
    bananax=[]
    bananay=[]
    cactusx=[]
    cactusy=[]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_DOWN:
            	vy = speed
            	wing.play()

            if event.type == KEYDOWN and event.key == K_UP:
            	vy = speed * -1
            	wing.play()


        # collision check
        response = collide(arrowx,arrowy,bombx,bomby,cactusx,cactusy)
        if response:
        	hit.play()
        	text_screen("Game Over", red, 5, 5)
        	text_screen("Your Score "+str(score), red, 25, 55)
        	pygame.display.update()
        	pygame.time.wait(3000)
        	return

        # update score
        update_score(applex,appley,bananax,bananay)

        text_screen("Score: " + str(score), red, 5, 5)
        pygame.display.update()
        # clock.tick(fps)

        many = many + vy
        if many<0 :
        	many = 0
        if many + manh > screen_height :
        	many = screen_height - manh


        SCREEN.blit(bgimg,(0,0))
        SCREEN.blit(man,(manx,many))

       	# pygame.time.wait(250)

       	choice=5
       	curtime=time.time()
       	if curtime-prevtime>2:
       		prevtime=curtime
       		choice = random.randint(0, 4)
       		# choice=2


        leftvel = -10

        bombx = [x + leftvel for x in bombx]
        applex = [x + leftvel for x in applex]
        arrowx = [x + leftvel for x in arrowx]
        bananax = [x + leftvel for x in bananax]
        cactusx = [x + leftvel for x in cactusx]



        if choice == 0 :
            x = screen_width - 50
            y = random.randint(0, screen_height-bombh)
            bombx.append(x)
            bomby.append(y)

        if choice == 1 :
            x = screen_width - 50
            y = random.randint(0, screen_height-appleh)
            applex.append(x)
            appley.append(y)

        if choice == 2 :
            x = screen_width - 50
            y = random.randint(0, screen_height-arrowh)
            arrowx.append(x)
            arrowy.append(y)

        if choice == 3 :
            x = screen_width - 50
            y = random.randint(0, screen_height-bananah)
            bananax.append(x)
            bananay.append(y)

       	if choice == 4 :
            x = screen_width - 50
            y = random.randint(0, screen_height-cactush)
            cactusx.append(x)
            cactusy.append(y)


        for x,y in zip(bombx,bomby):
        	SCREEN.blit(bomb,(x,y))

        for x,y in zip(applex,appley):
        	SCREEN.blit(apple,(x,y))

        for x,y in zip(arrowx,arrowy):
        	SCREEN.blit(arrow,(x,y))

        for x,y in zip(bananax,bananay):
        	SCREEN.blit(banana,(x,y))

        for x,y in zip(cactusx,cactusy):
        	SCREEN.blit(cactus,(x,y))

        pygame.display.update()
        clock.tick(fps)
    

    pygame.quit()
    quit()

def welcome():
    exit_game = False
    while not exit_game:
        SCREEN.fill((233,210,229))
        text_screen("Made by Aman Agrawal with love", black, 260, 250)
        text_screen("Press Space Bar To Play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pygame.mixer.music.load('back.mp3')
                    # pygame.mixer.music.play()
                    return

        pygame.display.update()
        clock.tick(fps)

while 1:
	welcome()
	gameloop()