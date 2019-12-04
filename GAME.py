import pygame
import os
import sys

# Still not fixed these, leave them for now.
WIDTH = 1280
HEIGHT = 600
PLAYER_HEIGHT = 20
PLAYER_WIDTH = 59
Level_select = 3
FPS = 60
ANIMATION = 10  # for when they move
clock = pygame.time.Clock()  # sets internal clock for the game
# Player life
LIFE = 200
TAKE_LIFE = 20
# Actions, these are good I found and because we have the FPS they should be consistent
GRAVITY = 10
MOVING_SPEED = 10
# Not used yet

JUMP_HEIGHT = 200  # This is actually double
PLAYER1_X = 500
PLAYER1_Y = 100

HIT_TIME = 100

pygame.init()

display_width = 1600
display_height = 800
screen = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)

GREY = (38,38,38)
BLACK = (0,0,0)

HERO1 = pygame.image.load(os.path.join('images', 'hero1.png')).convert()
HERO1.convert_alpha()
HERO1.set_colorkey(GREY)
HERO1L = pygame.transform.flip(HERO1, True, False)

HERO3 = pygame.image.load(os.path.join('images', 'hero3.png')).convert()
HERO3.convert_alpha()
HERO3.set_colorkey(BLACK)
HERO3 = pygame.transform.scale(HERO3, (50, 98))
HERO3L = pygame.transform.flip(HERO3, True, False)

VILLAIN1 = pygame.image.load(os.path.join('images', 'villain1.png')).convert()
VILLAIN1.convert_alpha()
VILLAIN1.set_colorkey(GREY)
VILLAIN1 = pygame.transform.scale(VILLAIN1, (60, 110))
VILLAIN1L = pygame.transform.flip(VILLAIN1, True, False)

VILLAIN2 = pygame.image.load(os.path.join('images', 'villain2.png')).convert()
VILLAIN2.convert_alpha()
VILLAIN2.set_colorkey(GREY)
VILLAIN2 = pygame.transform.scale(VILLAIN2, (60, 110))
VILLAIN2L = pygame.transform.flip(VILLAIN2, True, False)




class Platform(pygame.sprite.Sprite):
    # Defines size, position and colour of platform objects
    def __init__(self, size_x, size_y, pos_x, pos_y, colour):
        super().__init__()
        self.surface = pygame.Surface((size_x, size_y))
        self.rect = self.surface.get_rect(midtop=(pos_x, pos_y))
        self.surface.fill(colour)
        self.rect.x = pos_x
        self.rect.y = pos_y
    

        # draws the platform on the game screen

    def draw(self):
        screen.blit(self.surface, self.rect)


class Player(pygame.sprite.Sprite):
    # Probably need to add separate colours for each player, but then aagin we have the sprites?
    def __init__(self, x, y):
        super().__init__()
        # These are not used but DO NO CHANGE.
        self.image = pygame.Surface((0, 0))
        self.x = x
        self.y = y
        # the life rectangles for each player
        self.life = pygame.Rect(100, 100, LIFE, 30)
        self.life2 = pygame.Rect(1300, 100, LIFE, 30)
        # PLayer hitboxes
        self.hitbox = pygame.Rect(self.x, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
        self.hitbox2 = pygame.Rect(self.x + 400, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
        # Used in the jump function.
        self.jump1 = False
        self.jump2 = False
        self.jumpCount = JUMP_HEIGHT
        self.jumpCount2 = JUMP_HEIGHT
        # Hitting things
        self.hit = False
        self.hitCount = HIT_TIME
        self.arm = pygame.Rect(self.hitbox.x + 20, self.hitbox.y, 15, 5)
        self.dir = 1

        self.hit2 = False
        self.hitCount2 = HIT_TIME
        self.arm2 = pygame.Rect(self.hitbox.x + 20, self.hitbox.y, 15, 5)
        self.dir2 = -1
        # Updates the player, called after every action.

    def show(self, colour, screen, platforms, STAGE, bc):
        background_box = screen.get_rect()
        hit = False
        hit2 = False
        screen.blit(bc, background_box)
        for i in platforms:
            i.draw()
        pygame.draw.rect(screen, colour, self.life)
        pygame.draw.rect(screen, colour, self.life2)
        if self.hit:
            hit = True
            pygame.draw.rect(screen, pygame.Color("green"), self.arm)
        if self.hit2:
            hit2 = True
            pygame.draw.rect(screen, pygame.Color("green"), self.arm2)

        if hit2 is True:
            if self.dir2 == 1:
                screen.blit(VILLAIN2, self.hitbox2)
            else:
                screen.blit(VILLAIN2L, self.hitbox2)
        else:
            if self.dir2 == 1:
                screen.blit(VILLAIN1, self.hitbox2)
            elif self.dir2 == -1:
                screen.blit(VILLAIN1L, self.hitbox2)
        if hit is True:
            if self.dir == 1:
                screen.blit(HERO3, self.hitbox)
            else:
                screen.blit(HERO3L, self.hitbox)
        else:
            if self.dir == 1:
                screen.blit(HERO1, self.hitbox)
            elif self.dir == -1:
                screen.blit(HERO1L, self.hitbox)
            
    def falling(self,platforms):
        platforms = list(platforms)
        collision = False
        for i in range(len(platforms)):
    
            if self.hitbox.colliderect(platforms[i].rect):
        
                collision = True
                break
            
        collision2 = False
        for i in range(len(platforms)):
            if self.hitbox2.colliderect(platforms[i].rect):
                collision2 = True
                break
        
        if not collision and not self.jump1:
    
            self.hitbox.move_ip(0,GRAVITY)
        if not collision2 and not self.jump2:
            self.hitbox2.move_ip(0,GRAVITY)
            
    
    def reset(self):

        if self.hitbox.y >= 940:
    
            self.hitbox = pygame.Rect(self.x, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
            self.getHit(1)
           
        if self.hitbox2.y >= 940:
            self.hitbox2 = pygame.Rect(self.x + 400, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
            self.getHit(2)
          

        # Static move, can mess around with acceleration later

    def move(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.hitbox.move_ip(-MOVING_SPEED, 0)
         
            self.dir = -1
        if keys[pygame.K_d]:
            self.hitbox.move_ip(MOVING_SPEED, 0)
         
            self.dir = 1

        if keys[pygame.K_LEFT]:
            self.hitbox2.move_ip(-MOVING_SPEED, 0)
        
            self.dir2 = -1
        if keys[pygame.K_RIGHT]:
            self.hitbox2.move_ip(MOVING_SPEED, 0)
         
            self.dir2 = 1

        # Static jump, can mess around with equation later. We can try double jump later, shouldn't be too bad.

    def jump(self):

        if self.jump1:
            if self.jumpCount >= 0:
                self.hitbox.move_ip(0, -GRAVITY)
                self.jumpCount -= GRAVITY
             
# =============================================================================
#             elif self.jumpCount >= 0:
#                 self.hitbox.move_ip(0, GRAVITY)
#                 self.jumpCount -= GRAVITY
# =============================================================================
               
            else:
                self.jump1 = False
                self.jumpCount = JUMP_HEIGHT

        if self.jump2:
            if self.jumpCount2 >= 0:
                self.hitbox2.move_ip(0, -GRAVITY)
                self.jumpCount2 -= GRAVITY
              
# =============================================================================
#             elif self.jumpCount2 >= 0:
#                 self.hitbox2.move_ip(0, GRAVITY)
#                 self.jumpCount2 -= GRAVITY
# =============================================================================
              
            else:
                self.jump2 = False
                self.jumpCount2 = JUMP_HEIGHT

# Only hits in one direction. Potential solutions: implement direction? or implement 2 buttons to hit for each direction
    # Also arm isn't attached, it sort of drags behind, not sure how much of a problem it is.
    # Also no actual collsion yet.
    def hitting(self):
        global screen

        if self.hit:
            if self.hitCount >= 0:
                if self.dir == 1:
                    self.arm = pygame.Rect(self.hitbox.x + 20, self.hitbox.y, 15, 5)
                else:
                    self.arm = pygame.Rect(self.hitbox.x - 15, self.hitbox.y, 15, 5)
                # pygame.draw.rect(screen,pygame.Color('green') , arm)
                self.hitCount -= 5
              
            else:
                if self.arm.colliderect(self.hitbox2):
                    self.getHit(2)
                self.hit = False
                self.hitCount = HIT_TIME
            

        if self.hit2:
            if self.hitCount2 >= 0:
                if self.dir2 == 1:
                    self.arm2 = pygame.Rect(self.hitbox2.x + 20, self.hitbox2.y, 15, 5)
                else:
                    self.arm2 = pygame.Rect(self.hitbox2.x - 15, self.hitbox2.y, 15, 5)
                # pygame.draw.rect(screen,pygame.Color('green') , arm)
                self.hitCount2 -= 5
              
            else:
                if self.arm2.colliderect(self.hitbox):
                    self.getHit(1)
                self.hit2 = False
                self.hitCount2 = HIT_TIME
              

    # Gets called whenever the player gets hit and reduces that players life.
    def getHit(self, player):
        if player == 1:
            self.life.inflate_ip(-TAKE_LIFE, 0)
         
        if player == 2:
            self.life2.inflate_ip(-TAKE_LIFE, 0)
          

    # For this need a timer and a way to make the player flash?
    def invincible(self):
        pass


class Stage:

    def __init__(self, level_select):
        self.level_select = level_select

    def Level_load(self):
# =============================================================================
#         background = pygame.image.load(os.path.join('images', 'background' + str(Level_select) + '.png')).convert()
#         background_box = screen.get_rect()  # Fits background to screen
#         screen.blit(background, background_box)
# =============================================================================
        BLACK = (0, 0, 0)
        if self.level_select == 1:
            
            
            platforms = pygame.sprite.Group()
            platforms.add(Platform(WIDTH, 1, WIDTH // 2, HEIGHT - 100, (38, 38, 38)))
            platforms.add(Platform(300, 20, WIDTH // 1.95, HEIGHT // 3, BLACK))
            platforms.add(Platform(200, 20, WIDTH // 4, HEIGHT // 2, BLACK))
            platforms.add(Platform(200, 20, WIDTH // 1.3, HEIGHT // 2, BLACK))

        if self.level_select == 2:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(100, 20, WIDTH // 2.5, HEIGHT - 100, BLACK))
            platforms.add(Platform(100, 20, WIDTH // 1.4, HEIGHT - 100, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 1.8, HEIGHT - 230, BLACK))
            platforms.add(Platform(300, 20, WIDTH // 1.95, HEIGHT // 3, BLACK))
            platforms.add(Platform(200, 20, WIDTH // 4, HEIGHT // 2, BLACK))
            platforms.add(Platform(200, 20, WIDTH // 1.3, HEIGHT // 2, BLACK))

        if self.level_select == 3:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(150, 20, WIDTH // 2.65, HEIGHT // 1.75, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 1.6, HEIGHT // 1.75, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 2, HEIGHT // 4, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 1.1, HEIGHT // 1.75, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 9, HEIGHT // 1.75, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 4, HEIGHT // 1.3, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 1.3, HEIGHT // 1.3, BLACK))
            
        return platforms
            # Draws platforms
    def background_load(self):
        
        background = pygame.image.load(os.path.join('images', 'background' + str(self.level_select) + '.png')).convert()
        return background



def level1():
    main(1)
def level2():
    main(2)
def level3():
    main(3)


def main(level):
    SKY = (102, 178, 255)
    GREY = (38, 38, 38)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)  # Designated ALPHA colour, if you need something to exist but not be seen make it this colour
    bgColor = pygame.Color("white")
    fgColor = pygame.Color("black")
    plColor = SKY

    
    STAGE = Stage(level)
    level = STAGE.Level_load()
    bc = STAGE.background_load()
    # Initialise our players
    PLAYER = Player(PLAYER1_X, PLAYER1_Y)
    PLAYER.show(plColor, screen, level,STAGE,bc)
    
    while True:
        # all our events, might be worth putting into a method later, leave for now.
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                PLAYER.jump1 = True
            if e.key == pygame.K_UP:
                PLAYER.jump2 = True
            if e.key == pygame.K_s:
                PLAYER.hit = True
            if e.key == pygame.K_DOWN:
                PLAYER.hit2 = True
            if e.key == pygame.K_q:
                pygame.quit()
                sys.exit()
    
        clock.tick(FPS)
        # All the actions
        PLAYER.move()
        PLAYER.jump()
        PLAYER.falling(level)
        PLAYER.hitting()
        PLAYER.reset()
        # Update the display
        PLAYER.show(plColor, screen, level,STAGE,bc)
        pygame.display.update()





def quitgame():
    pygame.quit()
    quit()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
    
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
            
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    pygame.font.init()
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def mainMenu():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
              
                
        screen.fill(white)
        pygame.font.init()
        largeText = pygame.font.SysFont("comicsansms",90) 
        TextSurf, TextRect = text_objects("Smash Bros", largeText) 
        TextRect.center = ((display_width/2),(display_height*0.15)) 
        screen.blit(TextSurf, TextRect)

        button("Fight!",560,250,500,50,green,bright_green,stageMenu)
        button("Tutorial",560,350,500,50,green,bright_green,tutorialMenu)
        button("Quit",560,450,500,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)
        
        
def stageMenu():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(white) 
        largeText = pygame.font.SysFont("comicsansms",90) 
        TextSurf, TextRect = text_objects("Level Select", largeText) 
        TextRect.center = ((display_width/2),(display_height*0.15)) 
        screen.blit(TextSurf, TextRect)

        button("Stage 1",560,300,500,50,green,bright_green,level1)
        button("Stage 2",560,400,500,50,green,bright_green,level2)
        button("Stage 3",560,500,500,50,green,bright_green,level3)
        button("Menu",560,550,500,50,red,bright_red,mainMenu)

        pygame.display.update()
        clock.tick(15)
        
def tutorialMenu():
    tutorialPicture = pygame.image.load(os.path.join('images',"tutorialPicture.png")).convert() 
    #tutorialPicture = pygame.image.load("tutorialPicture.png") 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(white) 
        screen.blit(tutorialPicture,(365,0))  
        button("Menu",600,650,500,50,red,bright_red,mainMenu)

        pygame.display.update()
        clock.tick(15)
        
# =============================================================================
# def winnerScreen():
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#                 
#         screen.fill(grey) 
#         largeText = pygame.font.SysFont("comicsansms",90) 
#         #gameOver is whatever is outputted from gameplay
#         if gameOver == 1:
#             TextSurf, TextRect = text_objects("Player 1 wins!", largeText) 
#         elif gameOver == 2:
#             TextSurf, TextRect = text_objects("Player 2 wins!", largeText)
#         TextRect.center = ((display_width/2),(display_height*0.15)) 
#         screen.blit(TextSurf, TextRect)
# 
#         button("Menu",400,500,100,50,green,bright_green,mainMenu)
#         button("Quit",800,500,100,50,red,bright_red,quitgame)
# 
#         pygame.display.update()
#         clock.tick(15)
# =============================================================================
    
    
#pygame.init()
# =============================================================================
# display_width = 1600
# display_height = 800
# screen = gameScreen.screen
# =============================================================================

display_width = 1600
display_height = 800
screen = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
blue = (0,0,255)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
grey = (128,128,128)
 
block_color = (53,115,255)
 
 
pygame.display.set_caption("Smash Bros")
clock = pygame.time.Clock()

mainMenu()
pygame.quit()
quit()
