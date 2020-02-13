import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("太空侵略者")
# icon = pygame.image.load('spaceship.png')
# pygame.display.set_icon(icon)

background = pygame.image.load('background.png')
# 背景音乐
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

# spaceship
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 400
playerX_change = 0

# enemy
enemyImg = pygame.image.load('monster.png')
enemyX = random.randint(0, 735)
enemyY = 50
enemyX_change = 2
enemyY_change = 50

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 400
bulletY_change = 3
fire_bullet = False

# score
score_value = 0
font = pygame.font.Font("font.ttf", 32)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def bullet(x, y):
    global fire_bullet
    fire_bullet = True
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(bulletX, bulletY, enemyX, enemyY):
    c = math.sqrt(math.pow(bulletX - enemyX, 2) + math.pow(bulletY - enemyY, 2))
    if c < 27:
        return True
    else:
        return False


running = True
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                # 当按下空格键发射子弹，立即获取飞船X坐标
                # 之后再发射子弹
                if not fire_bullet:
                    # 加载射击音效
                    bullet_sound = mixer.Sound('shoot.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if enemyY > 550:
        # 制造一个新的怪物
        enemyX = random.randint(0, 735)
        enemyY = 50
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 2
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -2
        enemyY += enemyY_change

    if bulletY <= 0:
        bulletY = 400
        fire_bullet = False
    if fire_bullet:
        bulletY -= bulletY_change
        bullet(bulletX, bulletY)
    # 计算是否消灭怪物
    c = is_collision(bulletX, bulletY, enemyX, enemyY)
    if c and fire_bullet:
        fire_bullet = False
        bulletY = 400
        enemyX = random.randint(0, 735)
        enemyY = 50
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        score_value += 1
        # print(score)

    enemy(enemyX, enemyY)
    player(playerX, playerY)
    show_score(30, 20)
    pygame.display.update()



