import pygame
import sys
from pygame.locals import *
pygame.init()
clock=pygame.time.Clock()
size=width,height=1000,600
bg=(255,255,255)
speed=[-2,1]
fullscreen=False
screen=pygame.display.set_mode(size)
pygame.display.set_caption("初次见面，请大家多多关照!")

lead=pygame.image.load("乔治.png")
position=lead.get_rect()
l_head=lead
r_head=pygame.transform.flip(lead,True,False)


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type==KEYDOWN:
            #if event.key==K_LEFT and event.key==K_UP:
            #   speed=[-1,-1]
            # else:
                if event.key==K_LEFT:
                    lead = l_head
                    speed=[-1,0]
                if event.key==K_RIGHT:
                    lead = r_head
                    speed=[1,0]
                if event.key==K_UP:
                    speed=[0,-1]
                if event.key==K_DOWN:
                    speed=[0,1]
                if event.key==K_F11:
                    fullscreen=not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((1980,1024),FULLSCREEN | HWSURFACE )
                    else:
                        screen=pygame.display.set_mode(size)
    position=position.move(speed)
    if position.left<0 or position.right>width:

        lead=pygame.transform.flip(lead,True,True)
        speed[0]=-speed[0]
        
    if position.top<0 or position.bottom>height:
        speed[1]=-speed[1]

    
    screen.fill(bg)
    screen.blit(lead,position)
    pygame.display.flip()
    #pygame.time.delay(10)
    clock.tick(200)
