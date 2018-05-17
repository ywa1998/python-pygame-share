import pygame
import sys
import math
from pygame.locals import *
from random import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, grayball_image,greenball_image, position, speed, bg_size,target):
        
        pygame.sprite.Sprite.__init__(self)
        self.target=target
        self.grayball_image = pygame.image.load(grayball_image).convert_alpha()
        self.greenball_image = pygame.image.load(greenball_image).convert_alpha()
        self.rect = self.grayball_image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.width,self.height=bg_size[0],bg_size[1]
        self.radius=self.rect.width/2
        self.control=False
    def move(self):
        self.rect=self.rect.move(self.speed)

        if self.rect.right<0:
            self.rect.left=self.width
        elif self.rect.left>self.width:
            self.rect.right=0
        elif self.rect.bottom<0:
            self.rect.top=self.height
        elif self.rect.top>self.height:
            self.rect.bottom=0

    def check(self,motion):
        if self.target<motion<self.target + 5:
            return True
        else:
            return False 

    
class Glass(pygame.sprite.Sprite):
    def __init__(self,glass_image,mouse_image,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.glass_image=pygame.image.load(glass_image).convert_alpha()

        self.glass_rect=self.glass_image.get_rect()
        self.glass_rect.left,self.glass_rect.top=(bg_size[0]-self.glass_rect.width)//2,bg_size[1]-self.glass_rect.height
        self.mouse_image=pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect=self.mouse_image.get_rect()
        self.mouse_rect.left,self.mouse_rect.top=self.glass_rect.left,self.glass_rect.top
        pygame.mouse.set_visible(False)
        
def main():
    pygame.init()

    grayball_image = "gray_ball.png"
    greenball_image = "green_ball.png"
    bg_image = "background.png"
    glass_image="glass.png"
    mouse_image="hand.png"
    running = True
    gameOver=USEREVENT
    pygame.mixer.music.set_endevent(gameOver)
    bg_size = width, height = 1024, 681
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("Play the ball - FishC Demo")

    background = pygame.image.load(bg_image).convert_alpha()
    msgs=[]
    balls = []
    group=pygame.sprite.Group()
    hole = [(117, 119, 199, 201), (225, 227, 390, 392), \
            (503, 505, 320, 322), (698, 700, 192, 194), \
            (906, 908, 419, 421)]    

    pygame.mixer.music.load("hb.ogg")
    pygame.mixer.music.play()
    
    loser_sound=pygame.mixer.Sound("loser.wav")
    laugh_sound=pygame.mixer.Sound("laugh.wav")
    winner_sound=pygame.mixer.Sound("winner.wav")
    hole_sound=pygame.mixer.Sound("hole.wav")
    for i in range(5):
        position = randint(0, width-100), randint(0, height-100)
        speed = [randint(-10, 10), randint(-10, 10)]
        ball = Ball(grayball_image,greenball_image,position, speed, bg_size,5*(i+1))

        while pygame.sprite.spritecollide(ball,group,False,pygame.sprite.collide_circle):
            ball.rect.left,ball.rect.top=randint(0, width-100), randint(0, height-100)
        balls.append(ball)
        group.add(ball)

    glass=Glass(glass_image,mouse_image,bg_size)

    motion=0
    timer=USEREVENT+1
    pygame.key.set_repeat(100,100)
    pygame.time.set_timer(timer,1000)
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == gameOver:
                loser_sound.play()
                pygame.time.delay(2000)
                laugh_sound.play()
                running = False
            elif event.type==timer:
                 if motion:
                     for each in group:
                         if each.check(motion):
                             each.speed=[0,0]
                             each.control=True
                     motion=0
            elif event.type==MOUSEMOTION:
                motion+=1
            elif event.type==KEYDOWN:
                if event.key==K_w:
                    for each in group:
                        if each.control:
                            each.speed[1]-=1
                
                if event.key==K_s:
                    for each in group:
                        if each.control:
                            each.speed[1]+=1
           
                if event.key==K_a:
                    for each in group:
                        if each.control:
                            each.speed[0]-=1
           
                if event.key==K_d:
                    for each in group:
                        if each.control:
                            each.speed[0]+=1
                if event.key==K_SPACE:
                    for each in group:
                        if each.control:
                            for i in hole:
                                if i[0]<=each.rect.left<=i[1] and i[2]<=each.rect.top<=i[3]:
                                    hole_sound.play()
                                    each.speed=[0,0]
                                    group.remove(each)
                                    temp=balls.pop(balls.index(each))
                                    balls.insert(0,temp)
                                    hole.remove(i)
                            if not hole:
                                pygame.mixer.music.stop()
                                winner_sound.play()
                                pygame.time.delay(3000)
                                msg=pygame.image.load("win.png").convert_alpha()
                                msg_pos=(width-msg.get_width())//2,(height-msg.get_height())//2
                                msgs.append((msg,msg_pos))
                                laugh_sound.play()
                                    
                                            
        screen.blit(background, (0, 0))
        screen.blit(glass.glass_image,glass.glass_rect)

        glass.mouse_rect.left,glass.mouse_rect.top=pygame.mouse.get_pos()

        if glass.mouse_rect.left<glass.glass_rect.left:
            glass.mouse_rect.left=glass.glass_rect.left
            
        if glass.mouse_rect.left>glass.glass_rect.right-glass.mouse_rect.width:
            glass.mouse_rect.left=glass.glass_rect.right-glass.mouse_rect.width

        if glass.mouse_rect.top<glass.glass_rect.top:
            glass.mouse_rect.top=glass.glass_rect.top

        if glass.mouse_rect.bottom>glass.glass_rect.bottom-glass.mouse_rect.height:
            glass.mouse_rect.top=glass.glass_rect.bottom-glass.mouse_rect.height

        screen.blit(glass.mouse_image,glass.mouse_rect)
        
        for each in balls:
            each.move()
            if each.control:
                screen.blit(each.greenball_image, each.rect)
            else:
                screen.blit(each.grayball_image, each.rect)
            
        for each in group:
            group.remove(each)
            if pygame.sprite.spritecollide(each,group,False,pygame.sprite.collide_circle):
                each.speed[0]=-each.speed[0]
                each.speed[1]=-each.speed[1]

            group.add(each)
        for msg in msgs:
            screen.blit(msg[0],msg[1])
            
        pygame.display.flip()
        clock.tick(30)
        


if __name__=="__main__":
    main()
    

