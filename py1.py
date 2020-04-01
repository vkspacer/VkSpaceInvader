import pygame
import random
import math
from pygame import mixer

pygame.init()   #initalize the pygame
screen=pygame.display.set_mode((800,600))   #sets the geometry of window

pygame.display.set_caption("VKgaMes")   #it sets the title of pygame window
icon=pygame.image.load('ufo.png')   
pygame.display.set_icon(icon)   #sets icon of widow
bg=pygame.image.load('bg8.jpg')  #load the image

#ufo
x=370
y=480
px=0
img=pygame.image.load('fire.png')  #load the image
def player(xinc,yinc):
    screen.blit(img,(xinc,yinc))    #it write over the window

#creating multiple enemies
eimg=[]
ex=[]
ey=[]
ex_change=[]
ey_change=[]
n=6             #number of enemies
for i in range(n):    
    eimg.append(pygame.image.load('enemy.png'))
    ex.append(random.randint(0,735))
    ey.append(random.randint(50,150))
    ex_change.append(5)
    ey_change.append(40)

def enemy(ex,ey,i):
    screen.blit(eimg[i],(ex,ey))

#bullet
bulimg=pygame.image.load('bullet.png')
bulx=0
buly=480
bul_chgy=10
bulstate="ready"
def fire_bull(bullx,bully):
    global bulstate
    bulstate="fire"
    screen.blit(bulimg,(bullx+16,bully+10))

#collision
def iscol(ex,ey,bulx,buly):
    d=math.sqrt(pow((ex-bulx),2)+pow((ey-buly),2))
    if d<27:
        return True
    else:
        return False

#score
scoreval=0
font=pygame.font.Font('freesansbold.ttf',32)
tx=10
ty=10
def show_score(tx,ty):
    score=font.render("Score:"+str(scoreval),True,(255,255,255))
    screen.blit(score,(tx,ty))

#background music
mixer.music.load('bgmusic.mp3')
mixer.music.play(-1)
run=True

#GAME OVER 
vfont=pygame.font.Font('freesansbold.ttf',64)
def gameover():
    otext=vfont.render("GAME OVER",True,(255,0,0))
    screen.blit(otext,(200,250))
    score=font.render("Your Score:"+str(scoreval),True,(0,0,255))
    screen.blit(score,(300,350))

#main loop of game

while run:
    screen.fill((255,255,255))    #fill color in window
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                px=-3
            if event.key==pygame.K_RIGHT:
                px=3
            if event.key==pygame.K_SPACE:
                shoot=mixer.Sound('shoot.wav')
                shoot.play()
                if bulstate is "ready":
                    bulx=x
                    fire_bull(bulx,buly)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                px=0

    #movement of spaceship
    x+=px
    if x<=0:
        x=0
    if x>=736:
        x=736
    player(x,y)

    for i in range(n):
        #GAME OVER
        if ey[i]>400:
            for j in range(n):
                ey[j]=2000
            gameover()
            break
        #movement of enemy
        ex[i] += ex_change[i]
        if ex[i]<=0:
            ex_change[i]=5
            ey[i] += ey_change[i]
        elif ex[i]>=736:
            ex_change[i]=-3
            ey[i] += ey_change[i]

        #collision of enemy
        distance=iscol(ex[i],ey[i],bulx,buly)
        if distance:
            blast=mixer.Sound('explosion.wav')
            blast.play()    
            scoreval += 1
            buly=480
            bulstate="ready"
            ex[i]=random.randint(0,735)
            ey[i]=random.randint(50,150)
        enemy(ex[i],ey[i],i)

                    
    if bulstate is "fire":
        fire_bull(bulx,buly)
        buly -= bul_chgy
    if buly<=0:
        buly=480
        bulstate="ready"

    #display score on screen    
    show_score(tx,ty)    
    pygame.display.update()
