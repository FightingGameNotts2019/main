import pygame

WIDTH = 1600
HEIGHT = 800
PLAYER_HEIGHT = 20
PLAYER_WIDTH = 60
#might want to adjust the speeds on mac
FALLING_SPEED = 1
MOVING_SPEED = 1
#Not used yet
JUMP_HEIGHT = 100

class Player():
    
    def __init__(self, x,y, player):
        self.x = x
        self.y = y
        #This is player number, ie 1 or 2
        self.player = player
    def show(self,colour):
        global screen
        pygame.draw.rect(screen, colour, pygame.Rect(self.x,self.y,PLAYER_HEIGHT,PLAYER_WIDTH))
    
    def falling(self):
        global bgColor
        global plColor
        
        if self.x <= 400 - PLAYER_HEIGHT or self.x >= 1200:
            self.show(bgColor)
            self.y = self.y + FALLING_SPEED
            self.show(plColor)
        
    def reset(self):
        pass
        
    def move(self):
        global bgColor
        global plColor
        
        if self.player == 1:
            self.show(bgColor)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.x -= MOVING_SPEED
            if keys[pygame.K_d]:
                self.x += MOVING_SPEED
            self.show(plColor)
            
        if self.player == 2:
            self.show(bgColor)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.x -= MOVING_SPEED
            if keys[pygame.K_RIGHT]:
                self.x += MOVING_SPEED
            self.show(plColor)
        
        #Doesnt work
    def jump(self):
        global bgColor
        global plColor
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.y == 440:
                return
            self.show(bgColor)
            self.y -= FALLING_SPEED
            self.show(plColor)

    def hit(self):
        pass
    
    def getHit(self):
        pass
    
    def invincible(self):
        pass
    
    
    
class Stage():
    pass #?
    
    
    



pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

bgColor = pygame.Color("white")
fgColor = pygame.Color("black")
plColor = pygame.Color('red')
# filling the background
screen.fill(bgColor)

#fill this in stage
pygame.draw.rect(screen, fgColor, pygame.Rect(400,600,WIDTH/2,HEIGHT/20))

#Will change these numbers later to variables
PLAYER = Player(500,540,1)
PLAYER.show(plColor)

PLAYER2 = Player(1100, 540,2)
PLAYER2.show(plColor)
while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break

    # visualise the changes you just made
    pygame.display.flip()
    PLAYER.move()
    PLAYER.falling()
    
    PLAYER2.move()
    PLAYER2.falling()
    
    #PLAYER.jump()

pygame.quit() 