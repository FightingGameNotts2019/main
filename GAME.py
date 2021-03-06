import pygame
import os
import sys

# Still not fixed these, leave them for now.
WIDTH = 1200
HEIGHT = 600
PLAYER_HEIGHT = round(HEIGHT * 0.09)
PLAYER_WIDTH = round(WIDTH * 0.05)
FPS = 60
ANIMATION = 10  # for when they move
clock = pygame.time.Clock()  # sets internal clock for the game
# Player life
LIFE = 200
TAKE_LIFE = 20
# Actions, these are good I found and because we have the FPS they should be consistent
GRAVITY = 10
MOVING_SPEED = 8
# Not used yet

JUMP_HEIGHT = 200  # This is actually double
PLAYER1_X = WIDTH * 0.22
PLAYER1_Y = HEIGHT * 0.2

HIT_TIME = 100
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

punch_sound = pygame.mixer.Sound('punch.wav')
sword_sound = pygame.mixer.Sound('sword.wav')
music = pygame.mixer.Channel(0).play(pygame.mixer.Sound('game_music.wav'), -1)
GREY = (38, 38, 38)
BLACK = (0, 0, 0)

HERO1 = pygame.image.load(os.path.join('images', 'hero1.png')).convert()
HERO1.convert_alpha()
HERO1.set_colorkey(GREY)
HERO1 = pygame.transform.scale(HERO1, (PLAYER_WIDTH, round(PLAYER_HEIGHT * 1.4)))
HERO1L = pygame.transform.flip(HERO1, True, False)

HERO2 = pygame.image.load(os.path.join('images', 'hero2.png')).convert()
HERO2.convert_alpha()
HERO2.set_colorkey(GREY)
HERO2 = pygame.transform.scale(HERO2, (PLAYER_WIDTH, round(PLAYER_HEIGHT * 1.4)))
HERO2L = pygame.transform.flip(HERO2, True, False)

HERO3 = pygame.image.load(os.path.join('images', 'hero3.png')).convert()
HERO3.convert_alpha()
HERO3.set_colorkey(GREY)
HERO3 = pygame.transform.scale(HERO3, (PLAYER_WIDTH, round(PLAYER_HEIGHT * 1.4)))
HERO3L = pygame.transform.flip(HERO3, True, False)

VILLAIN1 = pygame.image.load(os.path.join('images', 'villain1.png')).convert()
VILLAIN1.convert_alpha()
VILLAIN1.set_colorkey(GREY)
VILLAIN1 = pygame.transform.scale(VILLAIN1, (PLAYER_WIDTH, round(PLAYER_HEIGHT * 1.4)))
VILLAIN1L = pygame.transform.flip(VILLAIN1, True, False)

VILLAIN2 = pygame.image.load(os.path.join('images', 'villain2.png')).convert()
VILLAIN2.convert_alpha()
VILLAIN2.set_colorkey(GREY)
VILLAIN2 = pygame.transform.scale(VILLAIN2, (PLAYER_WIDTH, round(PLAYER_HEIGHT * 1.4)))
VILLAIN2L = pygame.transform.flip(VILLAIN2, True, False)

VILLAIN3 = pygame.image.load(os.path.join('images', 'villain3.png')).convert()
VILLAIN3.convert_alpha()
VILLAIN3.set_colorkey(GREY)
VILLAIN3 = pygame.transform.scale(VILLAIN3, (PLAYER_WIDTH, round(PLAYER_HEIGHT * 1.4)))
VILLAIN3L = pygame.transform.flip(VILLAIN3, True, False)


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
    def __init__(self, player):

        super().__init__()
        self.player = player
        # These are not used but DO NO CHANGE.
       # self.image = pygame.Surface((0, 0))
        self.x = PLAYER1_X
        if self.player == 2:
            self.x = PLAYER1_X + (WIDTH * 0.58)
        self.y = PLAYER1_Y
        # the life rectangles for each player
        # PLayer hitboxes
        self.hitbox = pygame.Rect(self.x, self.y, PLAYER_HEIGHT, PLAYER_WIDTH * 1.2)
        # Used in the jump function.
        self.isjump = False
        self.jumpCount = JUMP_HEIGHT
        self.onGround = False
        # Hitting things
        self.hit = False
        self.hitCount = HIT_TIME
        self.arm = pygame.Rect(self.hitbox.x + 20, self.hitbox.y - (PLAYER_HEIGHT // 6), (WIDTH * 0.01), (HEIGHT * 0.01))

    def falling(self, platforms):
        platforms = list(platforms)
        collision = False
        for i in range(len(platforms)):

            if self.hitbox.colliderect(platforms[i].rect):

                collision = True
                break

        if not collision and not self.isjump:
            self.onGround = False
            self.hitbox.move_ip(0, GRAVITY)
        else:
            self.onGround = True

    def reset(self):

        if self.hitbox.y >= 940:
            self.hitbox = pygame.Rect(self.x, self.y, PLAYER_HEIGHT, PLAYER_WIDTH * 1.2)
            self.getHit()
        # Static move, can mess around with acceleration later
        # Static jump, can mess around with equation later. We can try double jump later, shouldn't be too bad.

    def jump(self):

        if self.isjump:
            if self.jumpCount >= 0:
                self.hitbox.move_ip(0, -GRAVITY)
                self.jumpCount -= GRAVITY
            else:
                self.isjump = False
                self.jumpCount = JUMP_HEIGHT

    # Only hits in one direction. Potential solutions: implement direction?
    # or implement 2 buttons to hit for each direction
    # Also arm isn't attached, it sort of drags behind, not sure how much of a problem it is.
    # Also no actual collsion yet.
    def hitting(self, player):
        global screen

        if self.hit:
            if self.hitCount >= 0:
                if self.dir == 1:
                    self.arm = pygame.Rect(self.hitbox.x + PLAYER_HEIGHT, self.hitbox.y + (PLAYER_WIDTH // 2),
                                           round((WIDTH * 0.005)), (HEIGHT * 0.01))
                else:
                    self.arm = pygame.Rect(self.hitbox.x - (WIDTH * 0.04), self.hitbox.y + (PLAYER_WIDTH // 2),
                                           round((WIDTH * 0.005)), (HEIGHT * 0.01))
                self.hitCount -= 5

            else:
                if self.arm.colliderect(player.hitbox):
                    player.getHit()
                self.hit = False
                self.hitCount = HIT_TIME

    # Gets called whenever the player gets hit and reduces that players life.
    def getHit(self):
        self.life = pygame.Rect(self.life.x,self.life.y,self.life.width - TAKE_LIFE, self.life.height)
        if self.life.width <= 0:
            winnerScreen(self.player)


    # For this need a timer and a way to make the player flash?
    def invincible(self):
        pass


class Player1(Player):
    def __init__(self, player):
        super().__init__(player)
        self.life = pygame.Rect(WIDTH * 0.03, HEIGHT * 0.14, WIDTH * 0.14, HEIGHT * 0.04)
        self.dir = 1

    def show(self, colour, screen):
        hit = False
        pygame.draw.rect(screen, bright_red, self.arm)
        pygame.draw.rect(screen, bright_green, self.hitbox)
        if self.life.width <= LIFE // 4:
            pygame.draw.rect(screen, bright_red, self.life)
        else:
            pygame.draw.rect(screen, bright_green, self.life)
        if self.hit:
            hit = True

        if hit is True:
            if self.dir == 1:
                screen.blit(VILLAIN3, self.hitbox)
                punch_sound.play()
            else:
                screen.blit(VILLAIN3L, self.hitbox)
                punch_sound.play()
        elif self.isjump:
            if self.dir == -1:
                screen.blit(VILLAIN2L, self.hitbox)
            else:
                screen.blit(VILLAIN2, self.hitbox)
        else:
            if self.dir == 1:
                screen.blit(VILLAIN1, self.hitbox)
            elif self.dir == -1:
                screen.blit(VILLAIN1L, self.hitbox)

    def move(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.hitbox.move_ip(-MOVING_SPEED, 0)

            self.dir = -1
        if keys[pygame.K_d]:
            self.hitbox.move_ip(MOVING_SPEED, 0)

            self.dir = 1


class Player2(Player):
    def __init__(self, player):
        super().__init__(player)
        self.life = pygame.Rect(WIDTH * 0.82, HEIGHT * 0.14, WIDTH * 0.14, HEIGHT * 0.04)
        self.dir = -1

    def show(self, colour, screen):
        hit = False
        pygame.draw.rect(screen, bright_red, self.arm)
        pygame.draw.rect(screen, bright_green, self.hitbox)
        if self.life.width <= LIFE // 4:
            pygame.draw.rect(screen, bright_red, self.life)
        else:
            pygame.draw.rect(screen, bright_green, self.life)
        if self.hit:
            hit = True
        if hit:
            if self.dir == 1:
                screen.blit(HERO3, self.hitbox)
                sword_sound.play()
            else:
                screen.blit(HERO3L, self.hitbox)
                sword_sound.play()
        elif self.isjump:
            if self.dir == -1:
                screen.blit(HERO2L, self.hitbox)
            else:
                screen.blit(HERO2, self.hitbox)
        else:
            if self.dir == 1:
                screen.blit(HERO1, self.hitbox)
            elif self.dir == -1:
                screen.blit(HERO1L, self.hitbox)

    def move(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.hitbox.move_ip(-MOVING_SPEED, 0)

            self.dir = -1
        if keys[pygame.K_RIGHT]:
            self.hitbox.move_ip(MOVING_SPEED, 0)

            self.dir = 1


class Stage:

    def __init__(self, level_select):
        self.level_select = level_select

    def Level_load(self):
        # =============================================================================
        #         background = pygame.image.load(os.path.join('images', 'background'
        #         + str(Level_select) + '.png')).convert()
        #         background_box = screen.get_rect()  # Fits background to screen
        #         screen.blit(background, background_box)
        # =============================================================================
        plat_height = HEIGHT * 0.03
        BLACK = (0, 0, 0)
        # All platforms are listed bottom to top as they would appear in a game level
        if self.level_select == 1:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(WIDTH, 1, 1, HEIGHT * 0.78, green))
            platforms.add(Platform(WIDTH * 0.2, plat_height, WIDTH * 0.67, HEIGHT * 0.5, BLACK))
            platforms.add(Platform(WIDTH * 0.2, plat_height, WIDTH * 0.17, HEIGHT * 0.5, BLACK))
            platforms.add(Platform(WIDTH * 0.2, plat_height, WIDTH * 0.42, HEIGHT * 0.33, BLACK))

        if self.level_select == 2:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(WIDTH * 0.08, plat_height, WIDTH * 0.63, HEIGHT * 0.86, BLACK))
            platforms.add(Platform(WIDTH * 0.08, plat_height, WIDTH * 0.32, HEIGHT * 0.86, BLACK))
            platforms.add(Platform(WIDTH * 0.12, plat_height, WIDTH * 0.45, HEIGHT * 0.67, BLACK))
            platforms.add(Platform(WIDTH * 0.16, plat_height, WIDTH * 0.71, HEIGHT * 0.5, BLACK))
            platforms.add(Platform(WIDTH * 0.16, plat_height, WIDTH * 0.17, HEIGHT * 0.5, BLACK))
            platforms.add(Platform(WIDTH * 0.24, plat_height, WIDTH * 0.39, HEIGHT * 0.33, BLACK))

        if self.level_select == 3:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(WIDTH * 0.16, plat_height, WIDTH * 0.43, HEIGHT // 1.3, BLACK))
            platforms.add(Platform(WIDTH * 0.24, plat_height, WIDTH * 0.09, HEIGHT // 1.75, BLACK))
           # platforms.add(Platform(WIDTH * 0.12, plat_height, WIDTH * 0.27, HEIGHT // 1.75, BLACK))
            platforms.add(Platform(WIDTH * 0.24, plat_height, WIDTH * 0.62, HEIGHT // 1.75, BLACK))
           # platforms.add(Platform(WIDTH * 0.12, plat_height, WIDTH * 0.82, HEIGHT // 1.75, BLACK))
            platforms.add(Platform(WIDTH * 0.16, plat_height, WIDTH * 0.43, HEIGHT // 4, BLACK))

        return platforms
        # Draws platforms

    def background_load(self):

        background = pygame.image.load(os.path.join('images', 'background' + str(self.level_select) + '.png')).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        return background

    def updateStage(self, screen, bc, platforms):
         background_box = screen.get_rect()
         screen.blit(bc, background_box)
         for i in platforms:
            i.draw()


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
    STAGE.updateStage(screen, bc, level)
    PLAYER = Player1(1)
    PLAYER2 = Player2(2)
    PLAYER2.show(plColor, screen)
    PLAYER.show(plColor, screen)

    while True:
        # all our events, might be worth putting into a method later, leave for now.
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            pygame.quit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w and PLAYER.onGround:
                PLAYER.isjump = True
            if e.key == pygame.K_UP and PLAYER2.onGround:
                PLAYER2.isjump = True
            if e.key == pygame.K_s:
                PLAYER.hit = True
            if e.key == pygame.K_DOWN:
                PLAYER2.hit = True
            if e.key == pygame.K_q:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)
        # All the actions
        PLAYER.move()
        PLAYER.jump()
        PLAYER.falling(level)
        PLAYER.hitting(PLAYER2)
        PLAYER.reset()
        # Update the display
        PLAYER2.move()
        PLAYER2.jump()
        PLAYER2.falling(level)
        PLAYER2.hitting(PLAYER)
        PLAYER2.reset()

        STAGE.updateStage(screen, bc, level)
        PLAYER.show(plColor, screen)
        PLAYER2.show(plColor, screen)
        pygame.display.update()


def quitgame():
    pygame.quit()
    quit()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    pygame.font.init()
    smallText = pygame.font.SysFont("comicsansms", 25)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


def mainMenu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(white)
        pygame.font.init()
        largeText = pygame.font.SysFont("comicsansms", 90)
        TextSurf, TextRect = text_objects("Byte Fight", largeText)
        TextRect.center = ((WIDTH / 2), (HEIGHT * 0.15))
        screen.blit(TextSurf, TextRect)

        button("Fight!", but_xpos, HEIGHT * 0.35, but_width, but_height, green, bright_green, stageMenu)
        button("Tutorial", but_xpos, HEIGHT * 0.5, but_width, but_height, green, bright_green, tutorialMenu)
        button("Quit", but_xpos, HEIGHT * 0.65, but_width, but_height, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


but_width = WIDTH * 0.4  # Width of all buttons
but_height = HEIGHT * 0.07  # Height of all buttons
but_xpos = (WIDTH // 2) - (but_width // 2)  # Position of all buttons (automatically centres)

def stageMenu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        largeText = pygame.font.SysFont("comicsansms", 90)
        TextSurf, TextRect = text_objects("Level Select", largeText)
        TextRect.center = ((WIDTH / 2), (HEIGHT * 0.15))
        screen.blit(TextSurf, TextRect)

        button("Stage 1", but_xpos, HEIGHT * 0.28, but_width, but_height, green, bright_green, level1)
        button("Stage 2", but_xpos, HEIGHT * 0.42, but_width, but_height, green, bright_green, level2)
        button("Stage 3", but_xpos, HEIGHT * 0.56, but_width, but_height, green, bright_green, level3)
        button("Menu", but_xpos, HEIGHT * 0.7, but_width, but_height, red, bright_red, mainMenu)

        pygame.display.update()
        clock.tick(15)


def tutorialMenu():
    tutorialPicture = pygame.image.load(os.path.join('images', "tutorialPicture.png")).convert()
    tutorialPicture = pygame.transform.scale(tutorialPicture, (round((WIDTH // 1.2)), round((HEIGHT // 1.6))))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        screen.blit(tutorialPicture, (WIDTH // 10, 0))
        button("Menu", but_xpos, HEIGHT * 0.8, but_width, but_height, red, bright_red, mainMenu)

        pygame.display.update()
        clock.tick(15)


def winnerScreen(winner):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(grey)
        largeText = pygame.font.SysFont("comicsansms",90)
        #gameOver is whatever is outputted from gameplay
        if winner == 1:
            TextSurf, TextRect = text_objects("Player 1 wins!", largeText)
        elif winner == 2:
            TextSurf, TextRect = text_objects("Player 2 wins!", largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT*0.15))
        screen.blit(TextSurf, TextRect)

        button("Menu", 400, 500, 100, 50, green, bright_green, mainMenu)
        button("Quit", 800, 500, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)



# pygame.init()
# =============================================================================

# screen = gameScreen.screen
# =============================================================================

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
blue = (0, 0, 255)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
grey = (128, 128, 128)

block_color = (53, 115, 255)

pygame.display.set_caption("Byte Fight")
clock = pygame.time.Clock()

mainMenu()
pygame.quit()
quit()
