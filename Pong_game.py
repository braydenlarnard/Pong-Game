# This is going to be a pong-type game

import pygame, sys, random
from pygame.locals import *


pygame.init()
CLOCK = pygame.time.Clock()
FPS = 30
WINDOWWIDTH = 900
WINDOWHEIGHT = 600
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
FONT = pygame.font.Font('freesansbold.ttf', 20)
pygame.display.set_caption('Pong')


# COLORS:   R       G       B
WHITE   = (255,     255,    255)
BLACK   = (0,       0,      0)
RED     = (255,     0,      0)
GREEN   = (0,       255,    0)
BLUE    = (0,       0,      255)
BGCOLOR = BLACK


# MAIN GAME LOOP
def main():
    running = True

    #define objects
    player1 = Paddle(20, 0, 10, 100, 10, WHITE)
    player2 = Paddle(WINDOWWIDTH-30, 0, 10, 100, 10, WHITE)
    ball = Ball(WINDOWWIDTH//2, WINDOWHEIGHT//2, 10, 7, WHITE)

    listOfPlayers = [player1, player2]

    #initial parameters of the players
    player1Score, player2Score = 0, 0
    player1YDirection, player2YDirection = 0, 0

    while running:
        SCREEN.fill(BLACK)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2YDirection = -1
                if event.key == pygame.K_DOWN:
                    player2YDirection = 1
                if event.key == pygame.K_w:
                    player1YDirection = -1
                if event.key == pygame.K_s:
                    player1YDirection = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2YDirection = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1YDirection = 0

        # Collision detection
        for player in listOfPlayers:
            if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                ball.hit()

        # Updates objects
        player1.update(player1YDirection)
        player2.update(player2YDirection)
        point = ball.update()

        # Scores points
        if point == -1:
            player1Score += 1
        elif point == 1:
            player2Score += 1

        # If a player scores a point the ball is reset
        if point:
            ball.reset()

        # Displays the objects on the screen
        player1.display()
        player2.display()
        ball.display()

        #Displaying the scores of the players
        player1.displayScore("Player 1: ", player1Score, 100, 20, WHITE)
        player2.displayScore("Player 2: ", player2Score, WINDOWWIDTH-100, 20, WHITE)

        pygame.display.update()
        # Adjusts the frame rate
        CLOCK.tick(FPS)


# Player class
class Paddle:
    def __init__(self, posx, posy, width, height, speed, color):
        # initializes position, size, speed, and color
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

        # Rect that is used to control position and collision
        self.obj = pygame.Rect(posx, posy, width, height)
        # Object that is blit on the screen
        self.objblit = pygame.draw.rect(SCREEN, self.color, self.obj)

        # function used to display object on screen
    def display(self):
        self.objblit = pygame.draw.rect(SCREEN, self.color, self.obj)

    # used to determine the movement of the paddle
    def update(self, yDirection):
        self.posy = self.posy + self.speed*yDirection

        # Restricts the paddle to be below the top of the screen
        if self.posy < 0:
                self.posy = 0
        # Restricts the paddle to be above the bottom of the screen
        elif self.posy > WINDOWHEIGHT-self.height:
            self.posy = WINDOWHEIGHT - self.height
            # updates the final values of itself
        self.obj = (self.posx, self.posy, self.width, self.height)

    # Used to render the player's score
    def displayScore(self, text, score, x, y, color):
        text = FONT.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        SCREEN.blit(text, textRect)

    def getRect(self):
        return self.obj

# Ball class
class Ball:
    # Initializes ball values
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xDirection = 1
        self.yDirection = -1
        self.ball = pygame.draw.circle(SCREEN, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    # displays the ball onto the screen
    def display(self):
        self.ball = pygame.draw.circle(SCREEN, self.color, (self.posx, self.posy), self.radius)

    # updates the ball on the screen
    def update(self):
        self.posx += self.speed*self.xDirection
        self.posy += self.speed*self.yDirection

        #If the ball hits the top or bottom, then it bounces
        if self.posy <= 0 or self.posy >= WINDOWHEIGHT:
            self.yDirection *= -1

        # If the ball hits the wall it indicates that the player has scored
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WINDOWWIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    # Resets the position of the ball to the center
    def reset(self):
        self.posx = WINDOWWIDTH//2
        self.posy = WINDOWHEIGHT//2
        self.xDirection *= -1
        self.firstTime = 1

    # Bounces the ball when hit
    def hit(self):
        self.xDirection *= -1

    #Gets the rect of the ball (for collisions)
    def getRect(self):
        return self.ball

if __name__ == "__main__":
    main()
    pygame.quit()
