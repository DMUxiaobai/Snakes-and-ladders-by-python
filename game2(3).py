"""Copyright (c) 2022, Lingyu Li, Shaoyang Wang and Yiwen Sun
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
"""
This is a simple game of snakes and ladders.
The game is played by 2 to 4 players.
Player can input their names.
The game is played on a board with 100 squares.
The players take turns to roll a dice.
The player moves forward the number of squares indicated by the dice.
If the player lands on the bottom of a ladder, the player moves up to the top of the ladder.
If the player lands on the head of a snake, the player moves down to the bottom of the snake.
The first player to reach the 100th square wins the game.
The winner's name is displayed on the screen.
The game can restart after the winner is displayed.
"""

from random import randint
import sndhdr   # for dice roll simulation  
import time     # for sleep function    
import sys      # for exit function
import pygame 
import PySimpleGUI as sg
from tkinter import * 
from tkinter import StringVar

class Player():
    """This class is used to create player objects.
    
    Attributes:
        name: A string representing the player's name.
        token_image: A string representing the player's token image.
        x: An integer representing the player's x co-ordinates.
        y: An integer representing the player's y co-ordinates.
        position: An integer representing the player's position on the board.
        isladder: A boolean representing whether the player is on a ladder.
        issnake: A boolean representing whether the player is on a snake.
        square_coordinates: A list of lists representing the co-ordinates of the squares on the board.
    """
    _red_token = pygame.image.load("red_token.png")
    _yellow_token = pygame.image.load("yellow_token.png")
    _green_token = pygame.image.load("green_token.png")
    _blue_token = pygame.image.load("blue_token.png")

    number_player = 0

    def __init__(self, name, token_image, x, y):
        self.name = name
        self.token_image = token_image
        self.position = 0
        self.isladder = False
        self.issnake = False
        self.x = x #initial x co-ordinates of the tokens.
        self.y = y    
        self.square_coordinates=[[406,606],
        [456,606],[506,606],[556,606],[606,606],[656,606],[706,606],[756,606],[806,606],[856,606],[906,606],
        [456,560],[506,560],[556,560],[606,560],[656,560],[706,560],[765,560],[806,560],[856,560],[906,560],
        [456,506],[506,506],[556,506],[606,506],[656,506],[706,506],[756,506],[806,506],[856,506],[906,506],
        [456,460],[506,460],[556,460],[606,460],[656,460],[706,460],[756,460],[806,460],[856,460],[906,460],
        [456,406],[506,406],[556,406],[606,406],[656,406],[706,406],[756,406],[806,406],[856,406],[906,406],
        [456,360],[506,360],[556,360],[606,360],[656,360],[706,360],[756,360],[806,360],[856,360],[906,360],
        [456,306],[506,306],[556,306],[606,306],[656,306],[706,306],[756,306],[806,306],[856,306],[906,306],
        [456,260],[506,260],[556,260],[606,260],[656,260],[706,260],[756,260],[806,260],[856,260],[906,260],
        [456,206],[506,206],[556,206],[606,206],[656,206],[706,206],[756,206],[806,206],[856,206],[906,206],
        [456,160],[506,160],[556,160],[606,160],[656,160],[706,160],[756,160],[806,160],[856,160],[906,160]]

    def message_display(self, text, x_position, y_position, size):   # function to display text
        largeText = pygame.font.SysFont("comicsansms", size)   # set the font and size
        TextSurf, TextRect = text_objects(text, largeText, WHITE)   # set the text
        TextRect.center = (x_position, y_position)   # set the text position
        SCREEN.blit(TextSurf, TextRect)   # display the text

    def dice_roll(self,a):
        global COMPUTER_TURN
        if a == 1:
            a = pygame.image.load("dice1.png").convert_alpha()
            number_a = "1"
        elif a == 2:
            a = pygame.image.load("dice2.png").convert_alpha()
            number_a = "2"
        elif a == 3:
            a = pygame.image.load("dice3.png").convert_alpha()
            number_a = "3"
        elif a == 4:
            a = pygame.image.load("dice4.png").convert_alpha()
            number_a = "4"
        elif a == 5:
            a = pygame.image.load("dice5.png").convert_alpha()
            number_a = "5"
        elif a == 6:
            a = pygame.image.load("dice6.png").convert_alpha()
            number_a = "6"
        time = pygame.time.get_ticks()  
        if COMPUTER_TURN == False:
            while time + 1000 > pygame.time.get_ticks():   # wait for 1 second
                SCREEN.blit(a, (140, 550))
                self.message_display("dice is: "+number_a, 200, 650, 30)
                pygame.display.update()

    def move(self):
        """Move the token according to the dice roll.
        
        If the token lands on a snake or ladder, move it to the
        appropriate square. Then display a message for 1 second.
        And if the token lands on a square greater than 100, move it
        back to the previous square. Then display a message for 1 second.
        Otherwise, display position of the token.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
        """
        dice = randint(1, 6)
        __display_dice_number = self.dice_roll(dice)  # display the dice number
        self.position += dice
        if self.position <= 100:
            lad = Ladder.judgeEvent(self.position)  # ladder
            if lad != self.position:
                self.isladder = True
                self.position = lad
            snk = Snake.judgeEvent(self.position)  # snake
            if snk != self.position:
                self.issnake = True
                self.position = snk
        else:
                self.position -= dice
                time = pygame.time.get_ticks() # get the time
                while time + 1000 > pygame.time.get_ticks():
                    self.message_display("You can't move", 650, 50, 35)
                    pygame.display.update()
                    
        self.x = self.square_coordinates[self.position][0]-25
        self.y = self.square_coordinates[self.position][1]-25
        if self.isladder:
            self.isladder = False
            time = pygame.time.get_ticks() # get the time
            while time + 500 > pygame.time.get_ticks():
                self.message_display("Ladder", 650, 50, 50)
                pygame.display.update()      
        if self.issnake:
            self.issnake = False
            time = pygame.time.get_ticks()
            while time + 500 > pygame.time.get_ticks():
                self.message_display("Snake", 650, 50, 50)
                pygame.display.update()
        if COMPUTER_TURN == False:
            time = pygame.time.get_ticks()
            while time + 500 > pygame.time.get_ticks():
                self.message_display(self.name+" is on square: "+str(self.position), 1150, 150, 30)
                pygame.display.update()
        else:
            time = pygame.time.get_ticks()
            while time + 500 > pygame.time.get_ticks():
                self.message_display("Computer is on square: "+str(self.position), 1150, 180, 30)
                pygame.display.update()

class Snake():
    """Class to check if the token lands on a snake or not.
    
    Attributes:
        None
    """
    def judgeEvent(place):
        if place == 25:
            return 5
        elif place == 34:
            return 1
        elif place == 47:
            return 19
        elif place == 65:
            return 52
        elif place == 87:
            return 57
        elif place == 91:
            return 61
        elif place == 99:
            return 69
        else:
            return place

class Ladder():
    """Class to check if the token lands on a ladder or not.
    
    Attributes:
        None
    """
    def judgeEvent(place):
        if place == 3:
            return 51
        elif place == 6:
            return 27
        elif place == 20:
            return 70
        elif place == 36:
            return 55
        elif place == 63:
            return 95
        elif place == 68:
            return 98
        else:
            return place

CLOCK = pygame.time.Clock() # for fps
pygame.init()  # initialize pygame
WIDTH = 1364     
HEIGHT = 768    
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # set the screen size
pygame.display.set_caption("Snakes and Ladders")  # set the screen title
FONT = pygame.font.SysFont("comicsansms", 30)  # set the font and size    
WINNER = "nobody"
COMPUTER_TURN = False

# set the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

# load the images
BOARD = pygame.image.load("board2.jpg")
INTRODUCTION = pygame.image.load("snake and ladder.jpg")
MENU_BACKGROUND = pygame.image.load("image1.png")
PLAY_BACKGROUD = pygame.image.load("image3.png")
WINNER_BACKGROUD = pygame.image.load("image2.png")
RED_TOKEN = pygame.image.load("red_token.png").convert_alpha()
YELLOW_TOKEN = pygame.image.load("yellow_token.png").convert_alpha()
GREEN_TOKEN = pygame.image.load("green_token.png").convert_alpha()
BLUE_TOKEN = pygame.image.load("blue_token.png").convert_alpha()

# set the players
PLAYER1 = Player("player1",RED_TOKEN,381,581)
PLAYER2 = Player("player2",YELLOW_TOKEN,356,581)
PLAYER3 = Player("player3",GREEN_TOKEN,331,581)
PLAYER4 = Player("player4",BLUE_TOKEN,306,581)

def message_display(text, x, y, size):  # text = text, x = x position, y = y position, size = size
    largeText = pygame.font.SysFont("comicsansms", size)  # set the font and size
    TextSurf, TextRect = text_objects(text, largeText, WHITE)  # set the text
    TextRect.center = (x, y)  # set the text position
    SCREEN.blit(TextSurf, TextRect)  # display the text

def text_objects(text, font, color):  # text = text, font = font, color = color
    textSurface = font.render(text, True, color)  # set the text
    return textSurface, textSurface.get_rect()  # return the text

# buttons function
def button(msg, x, y, w, h, i, fs, b): # msg = message, x = x position, y = y position, w = width, h = height, ic = inactive color, ac = active color, action = action
    """Create a button

    Create a button. When the mouse click on the button, it will do the action.

    Args:
        msg (str): The message on the button.
        x (int): The x position of the button.
        y (int): The y position of the button.
        w (int): The width of the button.
        h (int): The height of the button.
        i (tuple): The color of the button.
        fs (int): The font size of the message.
        b (str): The action of the button.
    
    Returns:
        b == "play": options()
        b == "quit": Quit()
        b == "back": initialise the players position and go to the menu
        b == "1 player": 1 player vs computer mode
        b == "2 players": 2 players mode
        b == "3 players": 3 players mode
        b == "4 players": 4 players mode
        b == "roll": roll the dice
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(SCREEN, i, (x, y, w, h))
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1 :
            if b == "play":
                PLAYER1.x = 381
                PLAYER1.y = 581
                PLAYER1.position = 0
                PLAYER2.x = 356
                PLAYER2.y = 581
                PLAYER2.position = 0
                PLAYER3.x = 331
                PLAYER3.y = 581
                PLAYER3.position = 0
                PLAYER4.x = 306
                PLAYER4.y = 581
                PLAYER4.position = 0
                options()
            elif b == "quit":              
                Quit()
            elif b == "back":
                PLAYER1.x = 381
                PLAYER1.y = 581
                PLAYER1.position = 0
                PLAYER2.x = 356
                PLAYER2.y = 581
                PLAYER2.position = 0
                PLAYER3.x = 331
                PLAYER3.y = 581
                PLAYER3.position = 0
                PLAYER4.x = 306
                PLAYER4.y = 581
                PLAYER4.position = 0
                return 7
            elif b == "1 player" :
                return 1
            elif b == "2 players":
                return 2
            elif b == "3 players":
                return 3
            elif b == "4 players":
                return 4
            elif b == "roll":
                return True
            else:
                return True
    message_display(msg, x + (w / 2), y + (h / 2), fs)

# Opening cover of the game
def intro():
    time = pygame.time.get_ticks() # get the time
    while time + 2000 > pygame.time.get_ticks(): # wait for 2 second
        SCREEN.blit(INTRODUCTION, (0, 0))
        pygame.display.update()

# quit function
def Quit():
    pygame.quit() # quit the game
    quit()

# Level 1 menu
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Quit()
        SCREEN.blit(WINNER_BACKGROUD, (0, 0)) # display the board
        button("PLAY", (WIDTH/2-200), (HEIGHT/2-120), 400, 100, GREEN, 60, "play") # display the play button\
        button("QUIT", (WIDTH/2-200), (HEIGHT/2+80), 400, 100, RED, 60, "quit") # display the quit button
        pygame.display.update() # update the screen

# winning screen
def win():
    global COMPUTER_TURN
    COMPUTER_TURN = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Quit()
        SCREEN.blit(MENU_BACKGROUND, (0, 0)) # display the board
        message_display(WINNER+" Wins", 650, 50, 50)
        button("PLAY", (WIDTH/2-200), (HEIGHT/2-120), 400, 100, GREEN, 60, "play") # display the play button\
        button("QUIT", (WIDTH/2-200), (HEIGHT/2+80), 400, 100, RED, 60, "quit") # display the quit button
        pygame.display.update() # update the screen

# Level 2 menu
def options():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Quit()
        b1=b2=b3=b4=b5= -1
        SCREEN.blit(MENU_BACKGROUND, (0, 0)) # display the board
        b1 = button("1 PLAYER", (WIDTH/2-150), 250, 300, 50, RED, 50, "1 player") # display the play button\
        b2 = button("2 PLAYER", (WIDTH/2-150), 350, 300, 50, YELLOW, 50, "2 players") # display the quit button
        b3 = button("3 PLAYER", (WIDTH/2-150), 450, 300, 50, GREEN, 50, "3 players") # display the quit button
        b4 = button("4 PLAYER", (WIDTH/2-150), 550, 300, 50, BLUE, 50, "4 players") # display the quit button
        b5 = button("BACK", 0, 650, 200, 50, PURPLE, 30, "back")# display the quit button
        if b5 == 7:
            main()
        if b1 == 1:
            play(21)
        if b2 == 2:
            play(2)
        if b3 == 3:
            play(3)
        if b4 == 4:
            play(4)
        pygame.display.update() # update the screen

# function to display the game is starting and one player's turn
def startgameing():
    time = pygame.time.get_ticks() # get the time
    while time + 2000 > pygame.time.get_ticks():
        message_display("Game is Starting. "+PLAYER1.name+"'s turn!", 650, 50, 50)
        pygame.display.update()

def play(number_of_players):
    """This function is used to play the game
    
    Let people enter their names and start the game
    According to the number of players, the game will be played differently mode
    Display every player's token, turn, position and dice number
    
    Args:
        number_of_players: the number of players
        
    Returns:
        None
    
    Raises:
        None
    """
    global WINNER
    global COMPUTER_TURN

    def submit():
        PLAYER1.name = var1.get()
        PLAYER2.name = var2.get()
        PLAYER3.name = var3.get()
        PLAYER4.name = var4.get()

    top = Tk()    
    top.title("Enter player names")
    screenwidth = top.winfo_screenwidth()
    screenheight = top.winfo_screenheight()
    top_width = 450
    top_height = 300
    top.geometry("%dx%d+%d+%d" % (top_width, top_height, 
                (screenwidth-top_width)/2, (screenheight-top_height)/2))
    var1 = StringVar()
    var2 = StringVar()
    var3 = StringVar()
    var4 = StringVar()
    Player1 = Label(top,text = "Player1").place(x = 40,y = 40)       
    Player2 = Label(top,text = "Player2").place(x = 40,y = 80)  
    Player3 = Label(top,text = "Player3").place(x = 40,y = 120) 
    Player4 = Label(top,text = "Player4").place(x = 40,y = 160) 
    Player1_input_area = Entry(top,width = 30, textvariable = 
                                var1).place(x = 130,y = 40)  
    Player2_input_area = Entry(top,width = 30, textvariable = 
                                var2).place(x = 130,y = 80)   
    Player3_input_area = Entry(top,width = 30, textvariable = 
                                var3).place(x = 130,y = 120)   
    Player4_input_area = Entry(top,width = 30, textvariable = 
                                var4).place(x = 130,y = 160)  
    submit_button = Button(top,text = "Submit",bd = '5',command = 
                            submit).place(x = 150,y = 200)  
    close_button = Button(top,text = "Close", bd = '5',command = 
                            top.destroy).place(x = 210,y = 200)
    top.mainloop() 

    SCREEN.blit(PLAY_BACKGROUD, (0, 0)) 
    SCREEN.blit(BOARD, (WIDTH/2-250,HEIGHT/2-250)) 
    SCREEN.blit(Player._red_token, (PLAYER1.x, PLAYER1.y)) 
    if 5>number_of_players>1 or number_of_players == 21:
        SCREEN.blit(Player._yellow_token, (PLAYER2.x, PLAYER2.y))
    if 5>number_of_players>2:
        SCREEN.blit(Player._green_token, (PLAYER3.x, PLAYER3.y))
    if 5>number_of_players>3:
        SCREEN.blit(Player._blue_token, (PLAYER4.x, PLAYER4.y))

    turn = 1  # to determine whose turn it is
    startgameing()  # display the game is starting and one player's turn

    while True:
        SCREEN.blit(PLAY_BACKGROUD, (0, 0)) 
        SCREEN.blit(BOARD, (WIDTH/2-250,HEIGHT/2-250)) 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Quit()

        if number_of_players == 21:
            if button(PLAYER1.name, 100, 700, 200 ,50 , RED, 30, "roll"):
                if turn == 1:
                    pygame.display.update()
                    PLAYER1.move()
                    COMPUTER_TURN = True
                    SCREEN.blit(PLAYER1._red_token, (PLAYER1.x, PLAYER1.y))
                    turn += 1
                    if PLAYER1.position == 100:
                        WINNER = PLAYER1.name
                        win()
                    if PLAYER1.position != 100:
                        time_delay = pygame.time.get_ticks()
                        while time_delay + 500 > pygame.time.get_ticks():
                            message_display("Computer's turn", 1150, 550, 30)
                            pygame.display.update() 
            button("Computer", 400, 700, 200,50,YELLOW,30,"roll")
            
            if True:
                if turn == 2:                 
                    PLAYER2.move()
                    COMPUTER_TURN = False
                    if number_of_players < 3 or number_of_players == 21:
                        turn = 1
                    if PLAYER2.position == 100:
                        WINNER = "computer"
                        win()
                    if PLAYER2.position != 100:
                        time_delay = pygame.time.get_ticks()
                        while time_delay + 2000 > pygame.time.get_ticks():
                            message_display(PLAYER1.name+"'s turn", 1150, 600, 30)
                            SCREEN.blit(PLAYER1._red_token, (PLAYER1.x, PLAYER1.y))
                            SCREEN.blit(PLAYER2._yellow_token, (PLAYER2.x+2, PLAYER2.y))
                            pygame.display.update()

        if 5>number_of_players>1:

            if button(PLAYER1.name, 100, 700, 200, 50, RED, 30, "roll"):
                button(PLAYER2.name, 400, 700, 200, 50, YELLOW, 30, "roll")
                if 4>number_of_players>2:
                    button(PLAYER3.name, 700, 700, 200,50,GREEN,30,"roll")
                if 5>number_of_players>3:
                    button(PLAYER3.name, 700, 700, 200,50,GREEN,30,"roll")
                    button(PLAYER4.name, 1000, 700, 200,50,BLUE,30,"roll")
                if turn == 1:
                    PLAYER1.move()
                    turn += 1
                    if PLAYER1.position == 100:
                        WINNER = PLAYER1.name
                        win()
                    if PLAYER1.position != 100:
                        time_delay = pygame.time.get_ticks()
                        while time_delay + 1000 > pygame.time.get_ticks():
                            PLAYER1.message_display(PLAYER2.name+"'s turn", 1150, 600, 30)
                            pygame.display.update()
                            
            if button(PLAYER2.name, 400, 700, 200, 50, YELLOW, 30, "roll"):
                if 4>number_of_players>2:
                    button(PLAYER3.name, 700, 700, 200,50, GREEN, 30, "roll")
                if 5>number_of_players>3:
                    button(PLAYER3.name, 700, 700, 200,50, GREEN, 30, "roll")
                    button(PLAYER4.name, 1000, 700, 200,50, BLUE, 30, "roll")
                if turn == 2:
                    PLAYER2.move()
                    turn += 1
                    time_delay = pygame.time.get_ticks()
                    if number_of_players < 3:
                        turn = 1
                    if PLAYER2.position == 100:
                        WINNER = PLAYER2.name
                        win()
                    if PLAYER2.position != 100:
                        if number_of_players == 2:
                            while time_delay + 1000 > pygame.time.get_ticks():
                                PLAYER2.message_display(PLAYER1.name+"'s turn", 1150, 600, 30)
                                pygame.display.update()
                        if number_of_players == 3:
                            while time_delay + 1000 > pygame.time.get_ticks():
                                PLAYER2.message_display(PLAYER3.name+"'s turn", 1150, 600, 30)
                                pygame.display.update()
                        if number_of_players == 4:
                            while time_delay + 1000 > pygame.time.get_ticks():
                                PLAYER2.message_display(PLAYER3.name+"'s turn", 1150, 600, 30)
                                pygame.display.update()
   
        if 5>number_of_players>2:
            if button(PLAYER3.name, 700, 700, 200,50,GREEN,30,"roll"):
                if 5>number_of_players>3:
                    button(PLAYER4.name, 1000, 700, 200,50, BLUE, 30, "roll")
                if turn == 3:
                    PLAYER3.move()
                    turn += 1
                    time_delay = pygame.time.get_ticks()
                    if number_of_players < 4:
                        turn = 1
                    if PLAYER3.position == 100:
                        WINNER = PLAYER3.name
                        win()
                    if PLAYER3.position != 100:
                        if number_of_players == 3:
                            while time_delay + 1000 > pygame.time.get_ticks():
                                PLAYER2.message_display(PLAYER1.name+"'s turn", 1150, 600, 30)
                                pygame.display.update()
                        if number_of_players == 4:
                            while time_delay + 1000 > pygame.time.get_ticks():
                                PLAYER2.message_display(PLAYER4.name+"'s turn", 1150, 600, 30)
                                pygame.display.update()

        if 5>number_of_players>3:
            if button(PLAYER4.name, 1000, 700, 200,50,BLUE,30,"roll"):
                if turn == 4:
                    PLAYER4.move()
                    turn += 1
                    time_delay = pygame.time.get_ticks()
                    if number_of_players < 5:
                        turn = 1
                    if PLAYER4.position == 100:
                        WINNER = PLAYER4.name
                        win()
                    if PLAYER4.position != 100:
                        while time_delay + 1000 > pygame.time.get_ticks():
                            PLAYER2.message_display(PLAYER1.name+"'s turn", 1150, 600, 30)
                            pygame.display.update()

        b6 = button("BACK", 0, 0, 200, 50 ,PURPLE,30,"back")
        if b6 == 7:
            options()
        SCREEN.blit(Player._red_token, (PLAYER1.x, PLAYER1.y)) 
        if 5>number_of_players>1 or number_of_players == 21:
            SCREEN.blit(Player._yellow_token, (PLAYER2.x+2, PLAYER2.y)) 
        if 5>number_of_players>2:
            SCREEN.blit(Player._green_token, (PLAYER3.x+4, PLAYER3.y))
        if 5>number_of_players>3:
            SCREEN.blit(Player._blue_token, (PLAYER4.x+6, PLAYER4.y))

        pygame.display.update()

intro()
main()
