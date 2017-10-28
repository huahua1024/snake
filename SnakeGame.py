#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import *
import pygame
from pygame.locals import *
from sys import exit
import time 

#定义窗口大小、蛇宽、颜色等
window_height = 320
window_width = 240
snake_color = (0, 0, 255)
blank_color = (255, 255, 255)
food_color = (255, 0, 0)
snake_height = 10
snake_width = 10
snake_rect = (snake_width, snake_height)
max_x_num = (window_width / snake_width) 
max_y_num = (window_height / snake_height)
print('max X,Y:', (max_x_num, max_y_num))

#初始化窗口
pygame.init()
screen = pygame.display.set_mode((window_height, window_width), 0, 32)
screen.fill((255,255,255))

#画蛇身，一个小方块
def draw_rect(scr, color, position, shape):
    pos = (position[1]*snake_height, position[0]*snake_width)
    pygame.draw.rect(scr, color, Rect(pos, shape))
    pygame.display.update()  

#定义贪吃蛇list，一个坐标点一个小方块
snake = [
    [max_x_num/4, max_y_num/4],
    [max_x_num/4, max_y_num/4-1],
    [max_x_num/4, max_y_num/4-2]
]

#初始化计数、第一个食物为固定坐标
score = 3
food = [max_x_num/2, max_y_num/2]
print('food position:', food)
draw_rect(screen, food_color, food, snake_rect)
pygame.display.set_caption('Score: ' + str(score))

#默认向右游动
key = K_RIGHT

#游戏开始
while True:
    #判断按键，上、下、左、右。并且判断冲突，例如：当前为上时，按下时忽略
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if (event.key==K_DOWN and key!=K_UP) or (event.key==K_UP and key!=K_DOWN) or (event.key==K_LEFT and key!=K_RIGHT) or (event.key==K_RIGHT and key!=K_LEFT):
                key = event.key
                
    # if snake[0][0] in [0, max_x_num-1] or snake[0][1] in [0, max_y_num-1] or snake[0] in snake[1:]:
    #     print('exit:', snake[0])
    #     exit()
    
    #仅蛇头碰蛇身，才判断为结束
    if snake[0] in snake[1:]:
        for n in snake:
            print('->', n)
        exit()

    #控制方向。碰到四周，从对面游出。
    new_head = [snake[0][0], snake[0][1]]
    if key == K_DOWN:
        # new_head[0] += 1 
        if new_head[0] < max_x_num-1:
            new_head[0] += 1
        else:
            new_head[0] = 0
    if key == K_UP:
        # new_head[0] -= 1 
        if new_head[0] > 0:
            new_head[0] -= 1
        else:
            new_head[0] =  max_x_num-1
    if key == K_LEFT:
        #new_head[1] -= 1
        if new_head[1] > 0:
            new_head[1] -= 1
        else:
            new_head[1] = max_y_num-1
    if key == K_RIGHT:
        #new_head[1] += 1
        if new_head[1] < max_y_num-1:
            new_head[1] += 1
        else:
            new_head[1] = 0    

    #插入新头部
    snake.insert(0,new_head)

    #判断是否吃到食物。如吃到，随机产生一新食物，计数加1。没吃到，则把蛇身去掉。
    if snake[0] == food:
        print('catch!', snake[0])
        score += 1
        pygame.display.set_caption('Score: ' + str(score))
        food = None
        while food is None:
            nf = [randint(1, max_x_num-2), randint(1, max_y_num-2)]    
            food = nf if nf not in snake else None
        draw_rect(screen, food_color, food, snake_rect)
    else:
        tail = snake.pop()
        draw_rect(screen, blank_color, tail, snake_rect)

    #每次仅绘制新头部。蛇身不变。
    draw_rect(screen, snake_color, snake[0], snake_rect)
    
    #每隔一定时间，更新一次。
    time.sleep(0.1)
    pygame.display.update()    
