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
PLAYER1_X = 500
PLAYER1_Y = 540
PLAYER2_X = 1100
PLAYER2_Y = 540


class Player():
    
    def __init__(self, x,y, player):
        self.x = x
        self.y = y
        #This is player number, ie 1 or 2
        self.player = player
        self.life = 200
        self.hitbox = pygame.Rect(self.x,self.y,PLAYER_HEIGHT,PLAYER_WIDTH)
        
    def showLife(self, color):
        global screen
        if self.player == 1:
            pygame.draw.rect(screen, color, pygame.Rect(100,100,self.life,30))
        elif self.player == 2:
            pygame.draw.rect(screen, color, pygame.Rect(1300,100,self.life,30))
        
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
            self.hitbox = pygame.Rect(self.x,self.y,PLAYER_HEIGHT,PLAYER_WIDTH)
        
    def reset(self):
        global plColor
        global bgColor
        
        if self.y == 940:
            if self.player == 1:
                self.show(bgColor)
                self.x = PLAYER1_X
                self.y = PLAYER1_Y
                self.show(plColor)
                self.showLife(bgColor)
                self.life -= 20
                self.showLife(plColor)
                self.hitbox = pygame.Rect(self.x,self.y,PLAYER_HEIGHT,PLAYER_WIDTH)
                
            elif self.player ==2:
                self.show(bgColor)
                self.x = PLAYER2_X
                self.y = PLAYER2_Y
                self.show(plColor)
                self.showLife(bgColor)
                self.life -= 20
                self.showLife(plColor)
                self.hitbox = pygame.Rect(self.x,self.y,PLAYER_HEIGHT,PLAYER_WIDTH)
        
    def move(self):
        global bgColor
        global plColor
        
        if self.player == 1:
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.show(bgColor)
                self.x -= MOVING_SPEED
            if keys[pygame.K_d]:
                self.show(bgColor)
                self.x += MOVING_SPEED
            self.hitbox = pygame.Rect(self.x,self.y,PLAYER_HEIGHT,PLAYER_WIDTH)
            self.show(plColor)
            
        if self.player == 2:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.show(bgColor)
                self.x -= MOVING_SPEED
            if keys[pygame.K_RIGHT]:
                self.show(bgColor)
                self.x += MOVING_SPEED
            self.hitbox = self.hitbox = pygame.Rect(self.x,self.y,PLAYER_HEIGHT,PLAYER_WIDTH)
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
STAGE = pygame.Rect(400,600,WIDTH/2,HEIGHT/20)
pygame.draw.rect(screen, fgColor, STAGE)

#Will change these numbers later to variables
PLAYER = Player(PLAYER1_X,PLAYER1_Y,1)
PLAYER.show(plColor)

PLAYER2 = Player(PLAYER2_X, PLAYER2_Y,2)
PLAYER2.show(plColor)
PLAYER.showLife(plColor)
PLAYER2.showLife(plColor)
while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break
    PLAYER.reset()
    PLAYER2.reset()
    # visualise the changes you just made
    pygame.display.flip()
    PLAYER.move()
    PLAYER.falling()
    
    
    PLAYER2.move()
    PLAYER2.falling()
    #PLAYER.jump()

pygame.quit() 