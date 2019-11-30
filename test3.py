import pygame

WIDTH = 1600
HEIGHT = 800
PLAYER_HEIGHT = 20
PLAYER_WIDTH = 59
FPS = 60
LIFE = 200
#might want to adjust the speeds on mac
FALLING_SPEED = 1
MOVING_SPEED = 1
#Not used yet
JUMP_HEIGHT = 100
PLAYER1_X = 500
PLAYER1_Y = 540



clock = pygame.time.Clock()


class Player():
    
    def __init__(self, x,y):
        #This is player number, ie 1 or 2
        self.x = x
        self.y = y
        self.life = pygame.Rect(100,100,LIFE,30)
        self.life2 = pygame.Rect(1300,100,LIFE,30)
        self.hitbox = pygame.Rect(self.x,self.y,PLAYER_HEIGHT,PLAYER_WIDTH)
        self.hitbox2 = pygame.Rect(self.x+400,self.y,PLAYER_HEIGHT,PLAYER_WIDTH)
        
        
    def show(self,colour,screen):
        global STAGE
        screen.fill((255,255,255))
        pygame.draw.rect(screen, pygame.Color("black"), STAGE)
        pygame.draw.rect(screen, colour, self.hitbox)
        pygame.draw.rect(screen, colour, self.hitbox2)
        pygame.draw.rect(screen, colour, self.life)
        pygame.draw.rect(screen, colour, self.life2)
        pygame.display.update()
    
    #Always falling now, cant fix one pixel being erased
    def falling(self):
        global plColor
        global STAGE
        
        if not self.hitbox.colliderect(STAGE):
            self.hitbox.move_ip(0,10)
            self.show(plColor,screen)
        if not self.hitbox2.colliderect(STAGE):
            self.hitbox2.move_ip(0,10)
            self.show(plColor,screen)
        
        
    def reset(self):
        global plColor
        
        if self.hitbox.y >= 940:
             self.hitbox = pygame.Rect(self.x,self.y,PLAYER_HEIGHT,PLAYER_WIDTH)
             self.life.inflate_ip(-20,0)
             self.show(plColor,screen)
        if self.hitbox2.y >= 940:
             self.hitbox2 = pygame.Rect(self.x+400,self.y,PLAYER_HEIGHT,PLAYER_WIDTH)
             self.life2.inflate_ip(-20,0)
             self.show(plColor,screen)
            
            
                
        
    def move(self):
        global plColor
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.hitbox.move_ip(-5,0)
            self.show(plColor,screen)
        if keys[pygame.K_d]:
            self.hitbox.move_ip(5,0)
            self.show(plColor,screen)
        
        if keys[pygame.K_LEFT]:
            self.hitbox2.move_ip(-5,0)
            self.show(plColor,screen)
        if keys[pygame.K_RIGHT]:
            self.hitbox2.move_ip(5,0)
            self.show(plColor,screen)
            
    
        
        #Doesnt work
# =============================================================================
#     def jump(self):
#         global bgColor
#         global plColor
#         
# 
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_w]:
#             if self.y == 440:
#                 return
#             self.show(bgColor)
#             self.y -= FALLING_SPEED
#             self.show(plColor)
#        #Doesnt work
#     def hit(self):
#         global screen
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_e]:
#         
#             arm = pygame.Rect(self.x+20,self.y, 15,5)
#             pygame.draw.rect(screen,pygame.Color('green') , arm)
#             self.hitbox.union(arm)
# =============================================================================
        
    
    def getHit(self):
        pass
    
    def invincible(self):
        pass
    
    
class Stage():
    pass #?
    
    
    



pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))


fgColor = pygame.Color("black")
plColor = pygame.Color('red')
# filling the background
screen.fill((255,255,255))

#fill this in stage
STAGE = pygame.Rect(400,600,WIDTH/2,HEIGHT/20)

#Will change these numbers later to variables
PLAYER = Player(PLAYER1_X,PLAYER1_Y)
PLAYER.show(plColor,screen)

#PLAYER.showLife(plColor)
#PLAYER2.showLife(plColor)
while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break
    clock.tick(FPS)
    # visualise the changes you just made
    PLAYER.move()
    PLAYER.falling()
    PLAYER.reset()
    pygame.display.flip()
    
    #PLAYER2.falling()
    #PLAYER.jump()

pygame.quit() 