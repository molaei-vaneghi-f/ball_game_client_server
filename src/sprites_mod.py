#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 12:46:25 2022
@author: f.molaei.vaneghi

module for handling:
    - game components (2 players and a ball), and
    - game logic (how players and ball move).
"""


import pygame, os, random

db_assets = os.path.join(os.path.dirname(os.path.realpath(__file__))+"/assets")

# variables
WHITE = (255,255,255)
FPS = 60

# Set up the drawing window
WINDOW_WIDTH, WINDOW_HEIGHT  = 800, 800  # in in pixels
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#%% classes

class Player():
    
    def __init__ (self, image_name, init_pos, speed_l, speed_r):
        
        # dimension/size of players images/avatars (identical and proportional to the size of the window)
        self.width, self.height = int(WINDOW_WIDTH/10), int(WINDOW_HEIGHT/10)
        
        # players images/avatars
        self.image_name = image_name
        self.image = pygame.image.load(os.path.join(db_assets,self.image_name))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        
        # players initial positions (tuple)
        # (0,0): top-left, (width, height): bottom-right
        self.init_pos = init_pos
        if self.init_pos == 'top':
            self.init_pos_h, self.init_pos_v = WINDOW_WIDTH/2, 0                           # center, top
        elif self.init_pos == 'bottom':
            self.init_pos_h, self.init_pos_v = WINDOW_WIDTH/2, WINDOW_HEIGHT - self.height # center, bottom
            
        # store the blit/current positiion of sprites/images i.e. players
        self.current_pos = pygame.Rect(self.init_pos_h, self.init_pos_v, self.width, self.height)
            
        # player step size (in pixels) when moving in R/L direction, increase for faster movement
        self.speed_l, self.speed_r = speed_l, speed_r
        
        
        
class Ball():
    
    def __init__(self, image_name, speed_x, speed_y):
       
        # dimension/size of the ball (proportional to the size of the window)
        self.width, self.height = int(WINDOW_WIDTH/20), int(WINDOW_HEIGHT/20)
        
        # ball image/avatar
        self.image_name = image_name
        self.image = pygame.image.load(os.path.join(db_assets,self.image_name))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        
        # ball initial position is chosen randomly                                                   
        # self.init_pos_h = random.randrange(self.width, WINDOW_WIDTH - self.width) 
        # self.init_pos_v = random.randrange(self.height, WINDOW_HEIGHT - self.height)  
        
        # ball initial position is at the center of the playground
        self.init_pos_h = WINDOW_WIDTH / 2
        self.init_pos_v = WINDOW_HEIGHT / 2

        # ball speed
        self.speed_x = speed_x
        self.speed_y = speed_y
        
        # store the blit/current positiion of sprites or images i.e. ball
        self.current_pos = pygame.Rect(self.init_pos_h, self.init_pos_v, self.width, self.height)  


#%% functions        

def draw_win_serv(player1, player2, ball, player2_current_pos_xy):
    
    """
    updates the screen by drawing sprites (images/texts) i.e. 2 players and a ball on it.
    """
    # fill the screen with white
    screen.fill(WHITE) 

    # tip: image or text are taken as surfaces to be shown on the screen using blit
    # draw players and the ball at positions represented by .x and .y
    screen.blit(player1.image, (player1.current_pos.x, player1.current_pos.y))
    screen.blit(player2.image, (player2_current_pos_xy[0], player2_current_pos_xy[1]))      
    screen.blit(ball.image, (ball.current_pos.x, ball.current_pos.y))

    # update the display/screen with what we have drawn
    # tip: .flip() updates the contents of the entire display => slower
    # tip: .update() updates a portion of the screen instead of the entire area of the screen when given an input argument => faster
        # without input args, updates the entire disply
    # pygame.display.flip()
    pygame.display.update() 
    
    
def draw_win_client(player1, player2, ball, pos_speed_from_server_list):    
        
    """
    updates the screen by drawing sprites (images/texts) i.e. 2 players and a ball on it.
    """
    screen.fill(WHITE) 

    screen.blit(player1.image, (pos_speed_from_server_list[0], pos_speed_from_server_list[1]))  
    screen.blit(player2.image, (player2.current_pos.x, player2.current_pos.y))
    screen.blit(ball.image, (pos_speed_from_server_list[2], pos_speed_from_server_list[3])) 

    pygame.display.update() 
    
    
def move_player(player):   
    
    """
    game logic for moving players.
    """
    
    # return a tuple with 0s and 1s representing the state of all keyboard keys AT EACH FRAME
    # note: for continous movement of the players:
        # 'keys' has to be placed in the game loop => gets updated at each frame.
        # and not in the event loop => gets updated ONLY when an event occurs e.g. a key is pressed.
    keys = pygame.key.get_pressed() 
    
    # if the left arrow key was oressed and ...: 
    # if keys[pygame.K_a] and player.current_pos.x > 0:                                       
    if keys[pygame.K_LEFT] and player.current_pos.x > 0:
        # move player 'player.speed_l' pixels to the left
        player.current_pos.x -= player.speed_l
        
    # if the right arrow key was oressed and ...: 
    # elif keys[pygame.K_d] and player.current_pos.x < sprites_mod.WINDOW_WIDTH - player2.width:
    elif keys[pygame.K_RIGHT] and player.current_pos.x < WINDOW_WIDTH - player.width:
        # move player 'player.speed_r' pixels to the right
        player.current_pos.x += player.speed_r   

        
def bouncing_ball(player1, player2, ball, player2_current_pos_xy):
    
    """
    game logic for moving the ball controlled by server.
    """

    # update the position of the ball  
    ball.current_pos.x += ball.speed_x
    ball.current_pos.y += ball.speed_y 
    
    # bouncing back with increased speed when hitting left_right walls
    if ball.current_pos.x > (WINDOW_WIDTH - ball.width) or ball.current_pos.x < 0:
        ball.speed_x = ball.speed_x*-1.5

    # upper-band (player 1)
    if ball.current_pos.y < player1.height: 
        # not-hitting the player1 on top
        if ball.current_pos.x < player1.current_pos.x or ball.current_pos.x > player1.current_pos.x + player1.width: 
            # do not bounce back from the top wall => player1 loses => game ends
            ball.speed_x = 0
            ball.speed_y = 0
        # bouncing back with increased speed hitting the player1 on top
        elif ball.current_pos.x > player1.current_pos.x and ball.current_pos.x < player1.current_pos.x + player1.width:
            # bounce back from player1 => game continues
            ball.speed_y = ball.speed_y*-1.5
            
    # lower-band (player 2)        
    elif ball.current_pos.y > WINDOW_HEIGHT - player1.height:  # assuming player 1 and 2 have the same height/width
        # not-hitting the player2 on botttom
        if ball.current_pos.x < player2_current_pos_xy[0] or ball.current_pos.x > player2_current_pos_xy[0] + player1.width:
            # do not bounce back from the bottom wall => player2 loses => game ends
            ball.speed_x = 0
            ball.speed_y = 0
            # bouncing back with increased speed hitting the player2 on bottom
        elif ball.current_pos.x > player2_current_pos_xy[0] and ball.current_pos.x < player2_current_pos_xy[0] + player1.width:
            # bounce back from player2 => game continues
            ball.speed_y = ball.speed_y*-1.5       
        
        
        
        
        
        
    