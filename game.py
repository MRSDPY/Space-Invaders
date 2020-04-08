import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

# set screen icon and title
pygame.display.set_caption("MR.SD Space Invaders")
icon = pygame.image.load('IMAGE/ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load('IMAGE/12.png')

# player space ship
player_img = pygame.image.load('IMAGE/spaceship.png')
playerPosX = 370
playerPosY = 500
playerMov = 0


def player(x, y):
    screen.blit(player_img, (x, y))


# enemy space ship
enemy_img = []
enemyPosX = []
enemyPosY = []
enemyMov = []
Number_Of_enemy = 5

for i in range(Number_Of_enemy):
    enemy_img.append(pygame.image.load('IMAGE/alien.png'))
    enemyPosX.append(random.randint(0, 736))
    enemyPosY.append(random.randint(40, 150))
    enemyMov.append(1.8)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# bullet
bullet_img = pygame.image.load('IMAGE/bullet.png')
bulletPosX = 0
bulletPosY = 500
bulletMov = 6
bullet_status = "loaded"


def bullet(x, y):
    global bullet_status
    bullet_status = "fire"
    screen.blit(bullet_img, (x + 19, y))


# For display score section
score = 0
font = pygame.font.Font('Font/Roboto-Black.ttf', 35)
scorePosX = 10
scorePosY = 10


def score_update(x, y):
    final_display_score = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(final_display_score, (x, y))


# For Display Game Over
game_over = pygame.font.Font('Font/Roboto-Black.ttf', 64)


def gameover():
    final_text = game_over.render("Game Over", True, (0, 255, 0))
    screen.blit(final_text, (200, 250))


# collision checker
def collision_status(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 25:
        return True
    else:
        return False


# this is running game loop
running_status = True
while running_status:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_status = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerMov -= 4
                # player_sound = pygame.mixer.music()
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerMov += 4
            if event.key == pygame.K_SPACE:
                if bullet_status == "loaded":
                    bullet_sound = mixer.Sound('Music/shoot.wav')
                    bullet_sound.play()
                    bulletPosX = playerPosX
                    bullet(bulletPosX, bulletPosY)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if bullet_status == "loaded":
                    bullet_sound = mixer.Sound('Music/shoot.wav')
                    bullet_sound.play()
                    bulletPosX = playerPosX
                    bullet(bulletPosX, bulletPosY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerMov = 0

    # for player
    playerPosX += playerMov
    if playerPosX <= 0:
        playerPosX = 0
    elif playerPosX >= 736:
        playerPosX = 736

    # for bullet
    if bulletPosY <= 0:
        bulletPosY = 500
        bullet_status = "loaded"

    if bullet_status == "fire":
        bullet(bulletPosX, bulletPosY)
        bulletPosY -= bulletMov

    # for enemy
    for i in range(Number_Of_enemy):
        enemyPosX[i] += enemyMov[i]
        if enemyPosX[i] <= 0:
            enemyMov[i] = 1.8
            enemyPosY[i] += 60
        elif enemyPosX[i] >= 736:
            enemyMov[i] = -1.8
            enemyPosY[i] += 60
        elif enemyPosY[i] > 450:
            for j in range(Number_Of_enemy):
                enemyPosY[j] = 2000
                gameover()
            break

        # check distance
        collision = collision_status(enemyPosX[i], enemyPosY[i], bulletPosX, bulletPosY)
        if collision:
            enemy_sound = mixer.Sound('Music/explosion.wav')
            enemy_sound.play()
            bulletPosY = 500
            bullet_status = "loaded"
            score += 1
            enemyPosX[i] = random.randint(0, 736)
            enemyPosY[i] = random.randint(40, 150)

        enemy(enemyPosX[i], enemyPosY[i], i)

    # function call section
    player(playerPosX, playerPosY)

    score_update(scorePosX, scorePosY)
    pygame.display.update()
