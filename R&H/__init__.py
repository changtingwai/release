# -*- coding: utf-8 -*-
import pygame
import math
import random
from pygame.locals import *


pygame.init()
w,h=640,480
keys=[False,False,False,False]
#角色位置
playerPos=[100,100]
screen=pygame.display.set_mode((w,h))

#箭支
#射击数量和命中獾次数
acc=[0,0]
#记录所有的箭支
arrows=[]

#敌人计时器，每隔段时间加一个新的敌人
badtimer=100
badtimer1=0
#敌人位置
badGuys=[[640,100]]
healthValue=194


healthBar=pygame.image.load("Resource/images/healthbar.png")    
health=pygame.image.load("Resource/images/health.png")   
gameover=pygame.image.load("Resource/images/gameover.png")
win=pygame.image.load("Resource/images/youwin.png")
arrow=pygame.image.load("Resource/images/bullet.png")
player=pygame.image.load("Resource/images/dude.png")
grass=pygame.image.load("Resource/images/grass.png")
castle=pygame.image.load("Resource/images/castle.png")
badGuysImg=pygame.image.load("Resource/images/badguy.png")
badGuysImg1=badGuysImg
goal=0
while 1:
    badtimer-=1
    #清屏
    screen.fill(0)
    #在屏幕上画草
    for x in range(w/grass.get_width()+1):
        for y in range(h/grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))
    #在屏幕上画角色
    position_mouse=pygame.mouse.get_pos()
    angle=math.atan2(position_mouse[1]-(playerPos[1]+32), position_mouse[0]-(playerPos[0]+26))
    playerRot=pygame.transform.rotate(player,360-angle*57.29)
    playerPos1=(playerPos[0]-playerRot.get_rect().w/2,playerPos[1]-playerRot.get_rect().h/2)
    
    
    screen.blit(playerRot,playerPos1)
    #画出城堡
    screen.blit(castle,(0,30))
    screen.blit(castle,(0,135))
    screen.blit(castle,(0,240))
    screen.blit(castle,(0,345))

    #画出箭支
    for bullet in arrows:
        index=0
        speed=10
        velx=math.cos(bullet[0])*speed
        vely=math.sin(bullet[0])*speed
        bullet[1]+=velx
        bullet[2]+=vely
        #子弹超出边界就消失
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index+=1
#         for projectile in arrows:
#             arrow1=pygame.transform.rotate(arrow,360-projectile[0]*57.29)
#             screen.blit(arrow1,(projectile[1],projectile[2]))
#             
        #转向后的箭支
        arrow1=pygame.transform.rotate(arrow,360-bullet[0]*57.29)
        screen.blit(arrow1,(bullet[1],bullet[2]))
    #画出敌人
    #计数器到时后，加入新敌人
    if badtimer==0:
        badGuys.append([640,random.randint(50,430)])
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index2=0
    for badguy in badGuys:
        if badguy[0]<-64:
            badGuys.pop(index2)
        badguy[0]-=3
        badrect=pygame.Rect(badGuysImg.get_rect())
        badrect.top=badguy[1]
        badrect.left=badguy[0]
        if badrect.left<64:
            #碰到城堡，减少生命值
            healthValue-=random.randint(5,20)
            badGuys.pop(index2)

        index1=0
        
        for bullet in arrows:
            bullRect=pygame.Rect(arrow.get_rect())
            bullRect.left=bullet[1]
            bullRect.top=bullet[2]
            if badrect.colliderect(bullRect):
                acc[0]+=1
                if index2>=0:
                    badGuys.pop(index2)
                    goal+=1
                if index1!=0:
                    arrows.pop(index1)
            index1+=1   
            
        index2+=1
    for badguy in badGuys:
        screen.blit(badGuysImg,badguy)
    #射击敌人
    

    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)
    #8 检测键盘
    if event.type==pygame.KEYDOWN:
        if event.key==K_w:
            keys[0]=True
        elif event.key==K_a:
            keys[1]=True
        elif event.key==K_s:
            keys[2]=True
        elif event.key==K_d:
            keys[3]=True 
    
    if event.type==pygame.KEYUP:
        if event.key==K_w:
            keys[0]=False
        elif event.key==K_a:
            keys[1]=False
        elif event.key==K_s:
            keys[2]=False
        elif event.key==K_d:
            keys[3]=False  
    
    #9移动角色
    if keys[0]:
        playerPos[1]-=3
    elif keys[2]:
        playerPos[1]+=3  
    elif keys[1]:
        playerPos[0]-=3
    elif keys[3]:
        playerPos[0]+=3
    
    #射箭
    if event.type==pygame.MOUSEBUTTONDOWN:
        position_mouse=pygame.mouse.get_pos()
        acc[1]+=1
        #将旋转角度,此时角色射出箭支位置记录到数组里
        arrows.append([math.atan2(position_mouse[1]-(playerPos1[1]+32),position_mouse[0]-(playerPos1[0]+26))\
                       ,playerPos1[0]+32,playerPos1[1]+32]) 
        
        
    #画生命条
    screen.blit(healthBar,(5,5))
    for health1 in range(healthValue):
        screen.blit(health,(health1+8,8))  
    #判断结束条件
    
    font=pygame.font.Font(None,24)
    text=font.render("kill enimy number:"+str(goal), True, (255,0,0))
    screen.blit(text,(400,0))
    if goal>20:
        screen.blit(win,(0,0)) 
    elif healthValue<0:
        screen.blit(gameover,(0,0)) 
    #更新屏幕       
    pygame.display.flip()