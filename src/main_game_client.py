"""
# game design:
    
    # the components of the game are:
        # playground in the form of square screen.
        # two players in the form of rectangular images of robots, one positioned on the top of the screen and the other on the bottom
        # a ball that can move within the boundaries of the screen (playground)
        
    # actions/movements of the components are:
        # each player can move either left or right.
        # the ball can move randomly within the boundaries of the screen, 
            # it bounces back when hitting the wall on the left/right or either of the players on top/bottom of the screen.
            # stops when hitting the wall on top/bottom of the screen (game ends!).
            
    # goal of the game is:
        # each player located on top/bottom of the screen should move (only to the left/right) in such a way:
            # to not allow the ball to hit the wall on top/bottom.
            # if that happens the player who missed the ball loses and the game ends.
            
    # server: controls movement of the ball as well as the player1 (top of the screen).
    # client: controls movement of the player2 (bottom of the screen).
    
Notes:
    - run the server script first, then the client.
    - when closing the scripts, first close the client script, then the servers' to prevent the folllowing error:
        - could not connect to the client: [Errno 98] Address already in use
        - solution: killall -9 python
"""

import pygame, sys
import sprites_mod
import client_server_mod

# initialize the game
pygame.init()
pygame.display.set_caption("I am Client, Let's Play!")

player1 = sprites_mod.Player('player1.png', 'top', 10, 10)       
player2 = sprites_mod.Player('player2.png', 'bottom', 10, 10)
ball = sprites_mod.Ball('ball.png', 2, 2)  
clien = client_server_mod.Clien()   
clien.connect()  

#%% main game

clock = pygame.time.Clock()
running = True

# game loop
while running:
    
    # with some delay send/receive position and speed values between client and server
    pygame.time.delay(10)
    # send current x position of player2/client to server
    clien.send_pos(player2)
    # run the game loop at FPS frames per second 
    clock.tick(sprites_mod.FPS)

    # move player1/client
    sprites_mod.move_player(player2)

    # event loop: for each event in the event_handling queue
    for event in pygame.event.get(): 
        # if the user clicked on the closed button => close the window and exit the game.
        if event.type == pygame.QUIT: 
            # running = False
            pygame.quit()                        
            sys.exit()
        
    # receive current x position of player1/server (and ball position and speed) 
    pos_speed_from_server_list = clien.rec_pos()

    # update the display with drawn rects        
    sprites_mod.draw_win_client (player1, player2, ball, pos_speed_from_server_list)

    
    






    
