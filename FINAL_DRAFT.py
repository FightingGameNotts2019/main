import pygame
import os
import sys

#Global Variables.

#Dimension variables
WIDTH = 1200
HEIGHT = 600
PLAYER_WIDTH = round(WIDTH * 0.05)
PLAYER_HEIGHT = round(HEIGHT * 0.14)

#Player attribute variables.
JUMP_HEIGHT = 200  
PLAYER1_X = WIDTH * 0.22    #Player starting positions.
PLAYER1_Y = HEIGHT * 0.2
GRAVITY = 10                #Attribute which decides the falling speed.
MOVING_SPEED = 8
LIFE = 200
TAKE_LIFE = 20              #Attribute which decides how much life players loose.
HIT_TIME = 100              #Attritbute which decides how long hit animations play.
ARM_WIDTH = (WIDTH * 0.005)
ARM_HEIGHT = (HEIGHT * 0.01)

#Game code variables.
FPS = 60
clock = pygame.time.Clock()  # sets internal clock for the game

pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

#Initialise the sounds and music in the game.
music = pygame.mixer.Channel(0).play(pygame.mixer.Sound('game_music.wav'), -1)
punch_sound = pygame.mixer.Sound('punch.wav')
sword_sound = pygame.mixer.Sound('sword.wav')
get_hit_sound = pygame.mixer.Sound('get_hit.wav')
pygame.mixer.music.set_volume(100)

#Initialise colours used in menus and gameplay.
GREY = (38, 38, 38)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
BROWN = (180, 143, 63)
block_color = (53, 115, 255)
CLOUD = (235, 235, 235)


#Fonts used for menus.
LARGE_TEXT = pygame.font.SysFont("comicsansms", 90)
SMALL_TEXT = pygame.font.SysFont("comicsansms", 25)

#Button dimensions.
BUT_WIDTH = WIDTH * 0.4  # Width of all buttons
BUT_HEIGHT = HEIGHT * 0.07  # Height of all buttons
BUT_XPOS = (WIDTH // 2) - (BUT_WIDTH // 2)  # Position of all buttons (automatically centres)

def make_img(var):
    var.convert_alpha()
    var.set_colorkey(GREY)
    var = pygame.transform.scale(var, (round(PLAYER_WIDTH*1.1), PLAYER_HEIGHT))
    return var

HERO1 = pygame.image.load(os.path.join('images', 'hero1.png')).convert()
HERO1 = make_img(HERO1)
HERO1L = pygame.transform.flip(HERO1, True, False)

HERO2 = pygame.image.load(os.path.join('images', 'hero2.png')).convert()
HERO2 = make_img(HERO2)
HERO2L = pygame.transform.flip(HERO2, True, False)

HERO3 = pygame.image.load(os.path.join('images', 'hero3.png')).convert()
HERO3 = make_img(HERO3)
HERO3L = pygame.transform.flip(HERO3, True, False)

VILLAIN1 = pygame.image.load(os.path.join('images', 'villain1.png')).convert()
VILLAIN1 = make_img(VILLAIN1)
VILLAIN1L = pygame.transform.flip(VILLAIN1, True, False)

VILLAIN2 = pygame.image.load(os.path.join('images', 'villain2.png')).convert()
VILLAIN2 = make_img(VILLAIN2)
VILLAIN2L = pygame.transform.flip(VILLAIN2, True, False)

VILLAIN3 = pygame.image.load(os.path.join('images', 'villain3.png')).convert()
VILLAIN3 = make_img(VILLAIN3)
VILLAIN3L = pygame.transform.flip(VILLAIN3, True, False)



#Class associated to the platforms players stand on.
class Platform(pygame.sprite.Sprite):
    # Defines size, position and colour of platform objects.
    def __init__(self, size_x, size_y, pos_x, pos_y, colour):
        super().__init__()
        self.surface = pygame.Surface((size_x, size_y))
        self.rect = self.surface.get_rect(midtop=(pos_x, pos_y))
        self.surface.fill(colour)
        self.rect.x = pos_x
        self.rect.y = pos_y

    #Draws the platforms.
    def draw(self):
        screen.blit(self.surface, self.rect)


#Class including general player attributes and actions.
class Player(pygame.sprite.Sprite):
    # Probably need to add separate colours for each player, but then aagin we have the sprites?
    def __init__(self, player):
        super().__init__()
        self.player = player
        #Player starting positions and dimensions.
        self.x = PLAYER1_X
        if self.player == 2:
            self.x = PLAYER1_X + (WIDTH * 0.58)
        self.y = PLAYER1_Y
        self.hitbox = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)    #Active area where the player can get hit.
        #Used in the jump function.
        self.isjump = False
        self.jumpCount = JUMP_HEIGHT
        self.onGround = False
        #Used in the hit fucntions.
        self.hit = False
        self.hitCount = HIT_TIME
        self.arm = pygame.Rect(self.hitbox.x + PLAYER_WIDTH, self.hitbox.y + (PLAYER_HEIGHT *0.6), ARM_WIDTH, ARM_HEIGHT)

    #Method which has the players constantly fall unless jumping or standing on a platform.
    def falling(self, platforms):
        platforms = list(platforms)
        collision = False
        #Check if the player is standing on a platform.
        for i in range(len(platforms)):
            if self.hitbox.colliderect(platforms[i].rect):
                collision = True
                break

        if not collision and not self.isjump:
            self.onGround = False
            self.hitbox.move_ip(0, GRAVITY)
        else:
            self.onGround = True
            
    #Resets the player to the starting position if he falls of the platforms, takes some life.
    def reset(self):
        if self.hitbox.y >= 940:
            self.hitbox = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
            self.getHit()
        

    #Method which when activated moves the player upwards based on jump height. Player falls back down using the falling method.
    def jump(self):
        if self.isjump:
            if self.jumpCount >= 0:
                self.hitbox.move_ip(0, -GRAVITY)
                self.jumpCount -= GRAVITY
            else:
                self.isjump = False
                self.jumpCount = JUMP_HEIGHT

    #Method responsible for attacks the players can do.
    def hitting(self, player):
       if self.hit:
            if self.hitCount >= 0:
                #Chooses the directions of the hit based on dir attribute.
                if self.dir == 1:
                    self.arm = pygame.Rect(self.hitbox.x + PLAYER_WIDTH, self.hitbox.y + (PLAYER_HEIGHT * 0.4),
                                           ARM_WIDTH, ARM_HEIGHT)
                else:
                    self.arm = pygame.Rect(self.hitbox.x - (WIDTH * 0.005), self.hitbox.y + (PLAYER_HEIGHT *0.4),
                                           ARM_WIDTH, ARM_HEIGHT)
                self.hitCount -= 5
            #Resets the arm back adn takes life from the enemy player if a collision was detected.
            else:
                if self.arm.colliderect(player.hitbox):
                    player.getHit()
                self.hit = False
                self.hitCount = HIT_TIME

    #Method which is called when this player is attacked and needs to loose life.
    def getHit(self):
        self.life = pygame.Rect(self.life.x,self.life.y,self.life.width - TAKE_LIFE, self.life.height)
        pygame.mixer.Channel(3).play(pygame.mixer.Sound(get_hit_sound), 0)
        #Checks if the player has any life left. Calls the winnerScreen method if any player died.
        if self.life.width <= 0:
            winnerScreen(self.player)

#Subclass for player1
class Player1(Player):
    def __init__(self, player):
        super().__init__(player)
        self.life = pygame.Rect(WIDTH * 0.03, HEIGHT * 0.14, WIDTH * 0.14, HEIGHT * 0.04)
        self.dir = 1
    
    #Method which updates the position of player 1 and adds the correct image for the sprite.
    def show(self, screen):
        hit = False
        #Use to check the player and arm hitboxes
        #pygame.draw.rect(screen, BRIGHT_GREEN, self.hitbox)
        #pygame.draw.rect(screen, BLUE, self.arm)
        #Draws the players life. Life bar turns red below 1/4 health
        if self.life.width <= LIFE // 4:
            pygame.draw.rect(screen, BRIGHT_RED, self.life)
        else:
            pygame.draw.rect(screen, BRIGHT_GREEN, self.life)
            
        #Updates the player when he is hitting. Has a unique image.
        if self.hit:
            hit = True
        if hit is True:
            if self.dir == 1:
                screen.blit(VILLAIN3, self.hitbox)
            else:
                screen.blit(VILLAIN3L, self.hitbox)
            punch_sound.play()
        #Updates the player when he is jumping, unique image.
        elif self.isjump:
            if self.dir == -1:
                screen.blit(VILLAIN2L, self.hitbox)
            else:
                screen.blit(VILLAIN2, self.hitbox)
        #Updates the player with the 'idle' image.
        else:
            if self.dir == 1:
                screen.blit(VILLAIN1, self.hitbox)
            elif self.dir == -1:
                screen.blit(VILLAIN1L, self.hitbox)
                
    #Player 1 movement method.
    def move(self):
        #Fetches the currently held keys.
        keys = pygame.key.get_pressed()
        #Moves the player an appropriate distance and updates the players direction.
        if keys[pygame.K_a]:
            self.hitbox.move_ip(-MOVING_SPEED, 0)
            self.dir = -1
        if keys[pygame.K_d]:
            self.hitbox.move_ip(MOVING_SPEED, 0)
            self.dir = 1

#Subclass for player 2
class Player2(Player):
    def __init__(self, player):
        super().__init__(player)
        self.life = pygame.Rect(WIDTH * 0.82, HEIGHT * 0.14, WIDTH * 0.14, HEIGHT * 0.04)
        self.dir = -1

    def show(self, screen):
        hit = False
        #Used to check the player and arm hitboxes
        #pygame.draw.rect(screen, BRIGHT_GREEN, self.hitbox)
        #pygame.draw.rect(screen, BLUE, self.arm)
        #Draws the players life. Life bar turns red below 1/4 health
        if self.life.width <= LIFE // 4:
            pygame.draw.rect(screen, BRIGHT_RED, self.life)
        else:
            pygame.draw.rect(screen, BRIGHT_GREEN, self.life)
            
        #Updates the player when he is hitting. Has a unique image.
        if self.hit:
            hit = True
        if hit:
            if self.dir == 1:
                screen.blit(HERO3, self.hitbox)
            else:
                screen.blit(HERO3L, self.hitbox)
            sword_sound.play()
        #Updates the player when he is jumping, unique image.
        elif self.isjump:
            if self.dir == -1:
                screen.blit(HERO2L, self.hitbox)
            else:
                screen.blit(HERO2, self.hitbox)
        #Updates the player with the 'idle' image.
        else:
            if self.dir == 1:
                screen.blit(HERO1, self.hitbox)
            elif self.dir == -1:
                screen.blit(HERO1L, self.hitbox)
    
    #Player 2 movement method.
    def move(self):
         #Fetches the currently held keys.
        keys = pygame.key.get_pressed()
        #Moves the player an appropriate distance and updates the players direction.
        if keys[pygame.K_LEFT]:
            self.hitbox.move_ip(-MOVING_SPEED, 0)
            self.dir = -1
            
        if keys[pygame.K_RIGHT]:
            self.hitbox.move_ip(MOVING_SPEED, 0)
            self.dir = 1

#Class for the stage on which the players play.
class Stage:
    def __init__(self, level_select):
        self.level_select = level_select

    #Method which returns the platforms of the chosen level.
    def Level_load(self):
        plat_height = HEIGHT * 0.03        
        #Adds the sequence which define the particular level.
        if self.level_select == 1:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(WIDTH, 1, 1, HEIGHT * 0.78, BROWN))
            platforms.add(Platform(WIDTH * 0.2, plat_height, WIDTH * 0.67, HEIGHT * 0.5, BLACK))
            platforms.add(Platform(WIDTH * 0.2, plat_height, WIDTH * 0.17, HEIGHT * 0.5, BLACK))
            platforms.add(Platform(WIDTH * 0.2, plat_height, WIDTH * 0.42, HEIGHT * 0.33, BLACK))

        if self.level_select == 2:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(WIDTH * 0.08, plat_height, WIDTH * 0.63, HEIGHT * 0.86, BLUE))
            platforms.add(Platform(WIDTH * 0.08, plat_height, WIDTH * 0.32, HEIGHT * 0.86, BLUE))
            platforms.add(Platform(WIDTH * 0.12, plat_height, WIDTH * 0.45, HEIGHT * 0.67, BLUE))
            platforms.add(Platform(WIDTH * 0.16, plat_height, WIDTH * 0.71, HEIGHT * 0.5, BLUE))
            platforms.add(Platform(WIDTH * 0.16, plat_height, WIDTH * 0.17, HEIGHT * 0.5, BLUE))
            platforms.add(Platform(WIDTH * 0.24, plat_height, WIDTH * 0.39, HEIGHT * 0.33, BLUE))

        if self.level_select == 3:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(WIDTH * 0.16, plat_height, WIDTH * 0.43, HEIGHT // 1.3, CLOUD))
            platforms.add(Platform(WIDTH * 0.24, plat_height, WIDTH * 0.09, HEIGHT // 1.75, CLOUD))
            platforms.add(Platform(WIDTH * 0.24, plat_height, WIDTH * 0.62, HEIGHT // 1.75, CLOUD))
            platforms.add(Platform(WIDTH * 0.16, plat_height, WIDTH * 0.43, HEIGHT // 4, CLOUD))

        return platforms
    
    #Loads and returns the background image with as a surface.
    def background_load(self):
        background = pygame.image.load(os.path.join('images', 'background' + str(self.level_select) + '.png')).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        return background

    #Draws the platform and background. Used to update the screen.
    def updateStage(self, screen, bc, platforms):
         background_box = screen.get_rect()
         screen.blit(bc, background_box)
         for i in platforms:
            i.draw()

#Functions used in the menu select to choose the appropriate level.
def level1():
    main(1)
def level2():
    main(2)
def level3():
    main(3)


def main(level):
    #Initialise and load the chosen Stage.
    STAGE = Stage(level)
    level = STAGE.Level_load()
    bc = STAGE.background_load()
    STAGE.updateStage(screen, bc, level)
    #Initialise and laod the PLayers.
    PLAYER = Player1(1)
    PLAYER2 = Player2(2)
    PLAYER2.show(screen)
    PLAYER.show(screen)
    #Main game loop.
    while True:
        #Initialise the events during the gameplay.
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            quitgame()
        #Events used to controle 'single' action controls: jumping and hitting for both players.
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w and PLAYER.onGround:
                PLAYER.isjump = True
            if e.key == pygame.K_UP and PLAYER2.onGround:
                PLAYER2.isjump = True
            if e.key == pygame.K_s:
                PLAYER.hit = True
            if e.key == pygame.K_DOWN:
                PLAYER2.hit = True
            #Used to quit the game during fullscreen.
            if e.key == pygame.K_q:
                quitgame()
                

        clock.tick(FPS)
        #Player 1 actions.
        PLAYER.move()
        PLAYER.jump()
        PLAYER.falling(level)
        PLAYER.hitting(PLAYER2)
        PLAYER.reset()
        #Player 2 actions
        PLAYER2.move()
        PLAYER2.jump()
        PLAYER2.falling(level)
        PLAYER2.hitting(PLAYER)
        PLAYER2.reset()
        #Update the screen with the actions players took.
        STAGE.updateStage(screen, bc, level)
        PLAYER.show(screen)
        PLAYER2.show(screen)
        pygame.display.update()

#Function used to quit the game if the player wants to quit from menu.
def quitgame():
    pygame.quit() 
    os._exit(0)

#Function used to create text in the menus.
def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

#Button function used to select items in the menus.
def button(msg, x, y, w, h, ic, ac, action=None):
    #Checks for mouse clicks.
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #Performs an action if a click was registered.
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    pygame.font.init()
    textSurf, textRect = text_objects(msg, SMALL_TEXT)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

#Main menu function which is called first when the player starts the game. Leads to the stage meu, tutorial menu or quit the game.
def mainMenu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
               
        
        #Menu graphics
        screen.fill(WHITE)
        pygame.font.init()
        TextSurf, TextRect = text_objects("Byte Fight", LARGE_TEXT)
        TextRect.center = ((WIDTH / 2), (HEIGHT * 0.15))
        screen.blit(TextSurf, TextRect)
        #The 3 options which the player can take in this menu.
        button("Fight!", BUT_XPOS, HEIGHT * 0.35, BUT_WIDTH, BUT_HEIGHT, GREEN, BRIGHT_GREEN, stageMenu)
        button("Tutorial", BUT_XPOS, HEIGHT * 0.5, BUT_WIDTH, BUT_HEIGHT, GREEN, BRIGHT_GREEN, tutorialMenu)
        button("Quit", BUT_XPOS, HEIGHT * 0.65, BUT_WIDTH, BUT_HEIGHT, RED, BRIGHT_RED, quitgame)

        pygame.display.update()
        clock.tick(FPS)


#Stage menu which lets the players select a level or go back to the main menu.
def stageMenu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        #Menu graphics.
        screen.fill(WHITE)
        TextSurf, TextRect = text_objects("Level Select", LARGE_TEXT)
        TextRect.center = ((WIDTH / 2), (HEIGHT * 0.15))
        screen.blit(TextSurf, TextRect)
        #Menu options.
        button("Safari", BUT_XPOS, HEIGHT * 0.31, BUT_WIDTH, BUT_HEIGHT, GREEN, BRIGHT_GREEN, level1)
        button("Forrest", BUT_XPOS, HEIGHT * 0.45, BUT_WIDTH, BUT_HEIGHT, GREEN, BRIGHT_GREEN, level2)
        button("Clouds", BUT_XPOS, HEIGHT * 0.59, BUT_WIDTH, BUT_HEIGHT, GREEN, BRIGHT_GREEN, level3)
        button("Menu", BUT_XPOS, HEIGHT * 0.73, BUT_WIDTH, BUT_HEIGHT, RED, BRIGHT_RED, mainMenu)

        pygame.display.update()
        clock.tick(FPS)

#Function called when the player wants to view the tutorial image.
def tutorialMenu():
    tutorialPicture = pygame.image.load(os.path.join('images', "tutorialPicture.png")).convert()
    tutorialPicture = pygame.transform.scale(tutorialPicture, (round((WIDTH // 1.2)), round((HEIGHT // 1.6))))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        #Return the player to the main menu.
        screen.fill(WHITE)
        screen.blit(tutorialPicture, (WIDTH // 10, 0))
        button("Menu", BUT_XPOS, HEIGHT * 0.8, BUT_WIDTH, BUT_HEIGHT, RED, BRIGHT_RED, mainMenu)

        pygame.display.update()
        clock.tick(FPS)

#Function called when one of the player win to congratulate the winning player.
def winnerScreen(winner):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        screen.fill(WHITE)
        #Winner attrtibute based on what player won the match.
        if winner == 1:
            TextSurf, TextRect = text_objects("Player 1 wins!", LARGE_TEXT)
        elif winner == 2:
            TextSurf, TextRect = text_objects("Player 2 wins!", LARGE_TEXT)
        TextRect.center = ((WIDTH/2),(HEIGHT*0.15))
        screen.blit(TextSurf, TextRect)
        #Lets the player return to the main menu or quit the game.
        button("Quit", BUT_XPOS, HEIGHT*0.65, BUT_WIDTH, BUT_HEIGHT, RED, BRIGHT_RED, quitgame)
        button("Menu", BUT_XPOS, HEIGHT*0.8, BUT_WIDTH, BUT_HEIGHT, GREEN, BRIGHT_GREEN, mainMenu)

        pygame.display.update()
        clock.tick(FPS)


pygame.display.set_caption("Byte Fight")
clock = pygame.time.Clock()
#Calls the main menu when the programm is started.
mainMenu()

