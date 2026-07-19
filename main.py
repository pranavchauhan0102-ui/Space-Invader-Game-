"""
Space Invader Game
------------------
Author: Pranav Chauhan

A classic Space Invader game built using Python and Pygame.

Features:
- Player movement
- Multiple enemies
- Bullet firing
- Collision detection
- Score system
- Background music
- Sound effects
- Game Over screen
"""


import pygame
import math
import random

from pygame import mixer

#initialising the game 
pygame.init()

#background
background=pygame.image.load('background.png')

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

#creating  the screen
screen = pygame.display.set_mode((800,600))

#title and icon
pygame.display.set_caption("Space Invader")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#creating the player
playerImg=pygame.image.load('playerImgFinal.png')
playerX=random.randint(0,750)
playerY=random.randint(500,600)
playerX_change=0
playerY_change=0

#creating the enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=4

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('play.png'))
    enemyX.append(random.randint(0,750))
    enemyY.append(random.randint(0,50))
    enemyX_change.append(0.2)
    enemyY_change.append(30)

'''#creating the enemy 
enemyImg=pygame.image.load('play.png')
enemyX=random.randint(0,750)
enemyY=random.randint(0,50)
enemyX_change=0.2
enemyY_change=30'''

#for bullet
bulletImg=pygame.image.load('bullet.png')
bulletX=playerX
bulletY=playerY
bulletX_change=0
bulletY_change=0.6
bullet_state="ready"

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))
    
def isCollision(w,x,y,z):
    distance=math.sqrt((math.pow(w-x,2))+ (math.pow(y-z,2)))
    if distance<=27:
        return True
    else:
        return False
    
def isGame_over(w,x,y,z):
    dist=math.sqrt((math.pow(w-x,2))+ (math.pow(y-z,2)))
    
    if dist<=30 or y > 550:
        return True
    else:
        return False

    
#displaying score on screen 

score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

def show_score(x,y):
    score=font.render("SCORE : "+ str(score_value) , True, (255,255,255) )
    screen.blit(score, (x,y))
    
#GAME over 
over_font=pygame.font.Font('freesansbold.ttf',64)

def game_over():
    over=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over,(200,250))

    

#Game logic
running=True
while running:

    #RGB (Red,Green,Blue)
    screen.fill((0,0,0))

    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #to detect if a key is pressed and if yes then what key was it and what will it do 
        if event.type==pygame.KEYDOWN:
            #print("Key is pressed")
            if event.key==pygame.K_UP:
                playerY_change=-0.3
            if event.key==pygame.K_DOWN:
                playerY_change=0.3
            if event.key==pygame.K_LEFT:
                playerX_change=-0.3
                #print("Left key is pressed ")
            if event.key==pygame.K_RIGHT:
                playerX_change= 0.3
                #print("Right key is pressed ")

            if event.key==pygame.K_SPACE:
                   if bullet_state=="ready": 
                     bullet_sound=mixer.Sound('laser.wav') 
                     bullet_sound.play()
                     bulletX=playerX
                     bulletY=playerY
                     fire_bullet(bulletX,bulletY)
                

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_DOWN or event.key==pygame.K_UP:
                playerY_change=0
                #print("Key is released")    


        

    playerX+=playerX_change
    playerY+=playerY_change

    # restricting the spaceship to go out of bounds
    if playerX<0:
        playerX=0
    elif playerX>736:
        playerX=736
    elif playerY<0:
        playerY=0
    elif playerY>536:
        playerY=536

    #enemy movement
    for i in range(num_of_enemies):
        
        if isGame_over(enemyX[i],playerX,enemyY[i],playerY):
            for j in range(num_of_enemies):
               enemyY[j]= 2000
            game_over()
            break

        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=0.2
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=768:
            enemyX_change[i]=-0.2
            enemyY[i]+=enemyY_change[i]

        collision=isCollision(enemyX[i],bulletX,enemyY[i],bulletY) 
        if collision:
            explosion_sound=mixer.Sound('explosion.wav') 
            explosion_sound.play()
            bulletX=playerX
            bulletY=playerY
            enemyX[i]=random.randint(0,750)
            enemyY[i]=random.randint(0,50)
            bullet_state="ready"   
            score_value+=1
            

        enemy(enemyX[i],enemyY[i],i)


    #bullet movement 
    if bullet_state =="fire":
         fire_bullet(bulletX,bulletY)
         bulletY-=bulletY_change
    if bulletY<=0:
        bullet_state="ready"
         

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
