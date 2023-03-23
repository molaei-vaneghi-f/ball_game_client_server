#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module for handling client and server

"""
import socket
import json 

#%% server

class Serv():
    
    def __init__(self):
        
        self.port = 8080
        self.pack_size = 1024*2  # bytes
        self.num_clients = 2
        
    def connect(self):
        
        try:
            # get the host name                                                                                                        
            self.host = socket.gethostname() 
            # get server instance
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('socket is created!')
            # bind host address and port together (takes tuple as input)
            self.server_sock.bind((self.host, self.port))
            print(f'socket is connected to this port: {self.port}!')
            # how many client the server can listen simultaneously
            self.server_sock.listen(self.num_clients)
            print(f'server socket is listening to {self.num_clients} clients ...')
            # accept new connection (server wait for client request)
            self.conn, self.addr = self.server_sock.accept()
            print(f'connection request was received from: {str(self.addr)}')
        
        except socket.error as error_msg:
            print("could not connect to the client:", error_msg)
            
    def disconnect(self):
        # a socket can not be reused once the connection is closed, i.e. you can not call socket.connect() on a closed socket. 
        print ('server socket is closed.')
        
      
    def send_pos(self, player1, ball):
        """
        send:
            - server/player1 current (x,y) position.
            - ball current (x,y) position.
            - ball current (x,y) speed.
        """
        
        send_to_client_list = []
        
        server_pos_text = "server current (x,y) position: " + "(" + str(player1.current_pos.x) + ',' + str(player1.current_pos.y) + ")" 
        ball_pos_text = "ball current (x,y) position: " + "(" + str(ball.current_pos.x) + ',' + str(ball.current_pos.y) + ")" 
        ball_speed_text = "ball current (x,y) speed: " + "(" + str(ball.speed_x) + ',' + str(ball.speed_y) + ")" 
        send_to_client_text = server_pos_text + '\n ' + ball_pos_text + '\n ' + ball_speed_text 
        send_to_client_list = [player1.current_pos.x, player1.current_pos.y, ball.current_pos.x, ball.current_pos.y, ball.speed_x, ball.speed_y]
        
        # using json for reading transferred data as string instead of bytes
        self.conn.send(json.dumps(send_to_client_list).encode('utf-8'))
        print (f' >>>>> sent to the client:\n {send_to_client_text}')
    
        return send_to_client_list
    
    def rec_pos(self):
        """
        receive x,y position of the client/player2.
        """
        
        # receive data stream, do not accept data packet greater than PACK_SIZE
        client_pos_xy_byte = self.conn.recv(self.pack_size) # byte
        # byte to list conversion
        tmp = str(client_pos_xy_byte).replace('b','').replace("'",'').replace('[','').replace(']','')
        client_pos_xy_list = list(tmp.split(','))
        client_pos_xy_list = [float(element) for element in client_pos_xy_list]
        print (f' <<<<<< received from the client:\n current x,y position: {client_pos_xy_list} ')
        
        # if data is not received (if client connection is closed), quit the server
        if not client_pos_xy_byte:
            # close the connection
            print('no data was received from the client => server connection is terminated.') 
            
        return client_pos_xy_list 

#%% client

class Clien():

    def __init__ (self):
        
        self.port = 8080
        self.pack_size = 1024*2  # bytes
    
    def connect(self):
        
        try:
            # get the host name                                                                                                        
            self.host = socket.gethostname()                                               
            # instantiate the client socket
            self.client_sock = socket.socket()
            # connect to the server (takes tuple as input), if unsuccessful print error message
            self.client_sock.connect((self.host, self.port))
            print('client socket connected')
       
        except socket.error as error_msg:
            print("could not connect to the server:", error_msg)    
            
    def disconnect(self):
        # close the connection when ball_speed_x is zero (game ended)
        self.client_sock.close()
        print ('closing the connection from the client side.')     
    
    
    def send_pos(self, player2):
        """
        send x,y position of the client/player2.
        """
        
        send_to_server_list = [player2.current_pos.x, player2.current_pos.y]
        client_pos_xy_text = str(player2.current_pos.x) + ',' + str(player2.current_pos.y)
        self.client_sock.send(json.dumps(send_to_server_list).encode('utf-8'))
        print(f'>>>>>> sent: client current x,y position: {client_pos_xy_text}')
        
        return send_to_server_list
        
    
    def rec_pos(self):
        """
        receive:
            - server/player1 current (x,y) position.
            - ball current (x,y) position.
            - ball current (x,y) speed.
        """
    
        pos_speed_from_server_str = self.client_sock.recv(self.pack_size).decode('utf-8') # string
        print(f'pos_speed_from_server_str: {pos_speed_from_server_str}')
        
        # changing server message from string to list
        pos_speed_from_server_list = pos_speed_from_server_str.replace('[','').replace(' ','').replace(']','')
        pos_speed_from_server_list = list(pos_speed_from_server_list.split(','))
        pos_speed_from_server_list = [float(element) for element in pos_speed_from_server_list]
        print(f'pos_speed_from_server_list: {pos_speed_from_server_list}')
    
        # print the received message 
        server_pos_text = "server current (x,y) position: " + "(" + str(pos_speed_from_server_list[0]) + ',' + str(pos_speed_from_server_list[1]) + ")" 
        ball_pos_text = "ball current (x,y) position: " + "(" + str(pos_speed_from_server_list[2]) + ',' + str(pos_speed_from_server_list[3]) + ")" 
        ball_speed_text = "ball current (x,y) speed: " + "(" + str(pos_speed_from_server_list[4]) + ',' + str(pos_speed_from_server_list[5]) + ")" 
        pos_speed_from_server_text = server_pos_text + '\n ' + ball_pos_text + '\n ' + ball_speed_text
        print(f'<<<<<< received: \n {pos_speed_from_server_text}')
       
        return pos_speed_from_server_list

    
    
    
