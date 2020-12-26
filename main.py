# Intialize the pygame
import pygame
import random
import math


pygame.init()
# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

#Background Sound
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change = 0.3
enemyY_change = 40

# Bullet
# Ready--cannot see the bullet on the screen/ Fire
bulletImg = pygame.image.load('bullet.png')
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"
bullet_speed = 200
bullet_current = 0
bulletlist = []

# Explosion
explosionImg = pygame.image.load('explosion.png')

# Score
scoreValue = 0
font = pygame.font.Font(None, 32)

textX = 10
textY = 10

# Game over text
over_font=pygame.font.Font(None, 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def showscore(x, y):
    score = font.render("Score :" + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    screen.blit(bulletImg, (x + 16, y - 10))


def explosion(x, y):
    screen.blit(explosionImg, (x, y))


# Game loop
running = True
while running:

    # RGB-Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                bullet_state = "fire"
                bullet_Sound=pygame.mixer.Sound('laser.wav')
                bullet_Sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                bullet_state = "ready"
                bullet_current = 0

    # checking for boundries of spaceship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # checking movement of enemy
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 0.3
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -0.3
        enemyY += enemyY_change

    if enemyY>200:
        enemyY=2000
        game_over_text()

    # Bullet movement
    if bullet_state == "fire":
        if bullet_current == 0 or bullet_current == bullet_speed:
            bullet_current = 1
            bullet = {
                "bulletX": playerX,
                "bulletY": 480
            }
            bulletlist.append(bullet)
        else:
            bullet_current += 1

    for i in bulletlist:
        if i.get("bulletY") <= 0:
            bulletlist.remove(i)
            continue
        fire_bullet(i.get("bulletX"), i.get("bulletY"))
        i["bulletY"] -= bulletY_change

    # dinimish enemy
    for i in bulletlist:
        if 100 >= math.sqrt((i.get("bulletX") - enemyX) ** 2 + (i.get("bulletY") - enemyY) ** 2):
            bulletlist.remove(i)
            scoreValue += 1
            explosion(enemyX, enemyY)
            enemyX = random.randint(0, 736)
            enemyY = random.randint(50, 150)
            collision_Sound=pygame.mixer.Sound('explosion.wav')
            collision_Sound.play()

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    showscore(textX, textY)
    pygame.display.update()
