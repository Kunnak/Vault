import sys
import pygame
import math
import random


# Fenstergröße
width = 1920
height = 1080

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Yannicks Spiel")

def main_game():
    global leben, score, anzahl, projectiles, enemies

    # Definieren der Schriftart und Größe
    font = pygame.font.Font(None, 36)

    # Definieren der Farben
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Spieler erstellen
    player_color = WHITE
    player_pos = [width / 2, height / 2]
    player_size = 25

    # Projektile erstellen
    projectiles = []
    projectile_color = (255, 0, 0)

    # Liste der Gegner
    enemies = []
    enemy_color = (255, 255, 255)
    enemy_speed = 0.1

    # Punkte erstellen
    score = 0

    # Leben erstellen
    leben = 3

    # maximale FPS
    clock = pygame.time.Clock()
    MAX_FPS = 1000

    # Floating Text bei Kollision
    floating_text = {"text": "+1", "position": [0, 0], "alpha": 255}

    # GAME OVER Schriftzug initialisieren
    font = pygame.font.Font(None, 50)
    game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(960, 240))

    # Anzahl wie viele Gegner aufgetreten sind
    anzahl = 0

    # Funktion zum Erstellen von Gegnern
    def spawn_enemy():
        # Zufällige Startposition des Gegners am Rand des Spielfeldes
        side = random.randint(1, 4)  # 1=links, 2=rechts, 3=oben, 4=unten
        if side == 1:
            start_pos = [random.randint(0, 20), random.randint(0, height)]
        elif side == 2:
            start_pos = [random.randint(width - 20, width), random.randint(0, height)]
        elif side == 3:
            start_pos = [random.randint(0, width), random.randint(0, 20)]
        else:
            start_pos = [random.randint(0, width), random.randint(height - 20, height)]


        # Richtung des Gegners
        direction = math.atan2(player_pos[1] - start_pos[1], player_pos[0] - start_pos[0])
        # Geschwindigkeit des Gegners
        speed = 0.1
        velocity = [speed * math.cos(direction), speed * math.sin(direction)]
        # Hinzufügen des Gegners zur Liste
        enemies.append([start_pos[0], start_pos[1], velocity[0], velocity[1]])
        pass

    # Funktion zur kontrolle ob Gegner und Spieler sich berühren
    def check_collision():
        global score, anzahl, leben
        pygame.init()
        # Überprüfen von Kollisionen zwischen Spieler und Gegnern
        for enemy in enemies:
            dist_player = math.sqrt((player_pos[0] - enemy[0]) ** 2 + (player_pos[1] - enemy[1]) ** 2)
            if dist_player < 30:
                enemies.remove(enemy)
                spawn_enemy()
                score = score - 10
                leben = leben - 1
                pass

        # Projektil-Kollision
        for projectile in projectiles:
            for enemy in enemies:
                distance = math.sqrt((projectile[0][0] - enemy[0]) ** 2 + (projectile[0][1] - enemy[1]) ** 2)
                if distance < 40:
                    enemies.remove(enemy)
                    projectiles.remove(projectile)
                    spawn_enemy()
                    score = score + 1
                    anzahl = anzahl + 1

                    break

    # Schleife für das Spiel
    while True:
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if leben == 0:
                        leben = 3
                        score = 0
                        anzahl = 0
                        enemies.clear()
                        projectiles.clear()
                        return True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Position des Mauszeigers
                mouse_pos = pygame.mouse.get_pos()
                # Richtung des Projektils
                direction = math.atan2(mouse_pos[1] - player_pos[1], mouse_pos[0] - player_pos[0])
                # Geschwindigkeit
                speed = 3
                # Geschwindigkeit in x- und y-Richtung berechnen
                velocity = [speed * math.cos(direction), speed * math.sin(direction)]
                # Hinzufügen des Projektils zur Liste
                projectiles.append([list(player_pos), velocity])

        if leben > 0:
            # Hintergrundfarbe
            screen.fill((0, 0, 0))

            # Spieler zeichnen
            pygame.draw.rect(screen, player_color,
                             [player_pos[0] - player_size / 2, player_pos[1] - player_size / 2, player_size,
                              player_size])

            # Projektile zeichnen
            for projectile in projectiles:
                pygame.draw.circle(screen, projectile_color, [int(projectile[0][0]), int(projectile[0][1])], 12)
                projectile[0][0] += projectile[1][0]
                projectile[0][1] += projectile[1][1]

                # Entfernen der Projektile am Rand
                if projectile[0][0] < 0 or projectile[0][0] > width or projectile[0][1] < 0 or projectile[0][
                    1] > height:
                    projectiles.remove(projectile)

            # Gegner erstellen
            if len(enemies) < 6 and anzahl <= 10:
                spawn_enemy()
                enemy_speed = 0.15
            if len(enemies) < 7 and anzahl > 20:
                spawn_enemy()
                enemy_speed = 0.2
            if len(enemies) < 9 and anzahl >= 50:
                spawn_enemy()
                enemy_speed = 0.3
            if len(enemies) < 10 and anzahl >= 100:
                spawn_enemy()
                enemy_speed = 0.4
            if len(enemies) < 10 and anzahl >= 200:
                spawn_enemy()
                enemy_speed = 0.5
            if len(enemies) < 10 and anzahl >= 300:
                spawn_enemy()
                enemy_speed = 0.6
            if len(enemies) < 10 and anzahl >= 400:
                spawn_enemy()
                enemy_speed = 0.7
            if len(enemies) < 10 and anzahl >= 500:
                spawn_enemy()
                enemy_speed = 0.8
            if len(enemies) < 10 and anzahl >= 600:
                spawn_enemy()
                enemy_speed = 0.9
            if len(enemies) < 10 and anzahl >= 700:
                spawn_enemy()
                enemy_speed = 1
            if len(enemies) < 10 and anzahl >= 800:
                spawn_enemy()
                enemy_speed = 1.1
            if len(enemies) < 10 and anzahl >= 900:
                spawn_enemy()
                enemy_speed = 1.2
            if len(enemies) < 10 and anzahl >= 1000:
                spawn_enemy()
                enemy_speed = 1.3

            # Gegner zeichnen und bewegen
            for enemy in enemies:
                pygame.draw.circle(screen, enemy_color, [int(enemy[0]), int(enemy[1])], 35)

                # Bewegen des Gegners in Richtung Spieler
                direction = math.atan2(player_pos[1] - enemy[1], player_pos[0] - enemy[0])
                velocity = [enemy_speed * math.cos(direction), enemy_speed * math.sin(direction)]
                enemy[0] += velocity[0]
                enemy[1] += velocity[1]


            check_collision()

            # Aktualisieren und Zeichnen der Punktzahl
            score_text = font.render("Score: " + str(score), True, WHITE)
            leben_text = font.render("Leben: " + str(leben), True, WHITE)
            screen.blit(score_text, [20, 10])
            screen.blit(leben_text, [20, 50])

            # Update des Bildschirms
            pygame.display.update()


        else:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if leben == 0:
                                leben = 3
                                score = 0
                                anzahl = 0
                                enemies.clear()
                                projectiles.clear()
                                return True

                # Game Over Text
                screen.blit(game_over_text, game_over_rect)
                pygame.display.update()
                score_text = font.render("Score: " + str(score), True, WHITE)
                screen.blit(score_text, [870, 300])
                wiederholen_text = font.render("Mit Leertaste Spiel neustarten !", True, WHITE)
                screen.blit(wiederholen_text, [690, 950])

def run_game():
    while True:
        main_game()

#Aufruf der main_game() Funktion
run_game()