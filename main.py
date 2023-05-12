import sys
import pygame
import math
import random


# Fenstergröße
width = 800
height = 800

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
    enemy_size = 40

    # Punkte erstellen
    score = 0

    # Leben erstellen
    leben = 3

    # maximale FPS
    clock = pygame.time.Clock()
    MAX_FPS = 60

    # Soundeffekte
    pygame.mixer.init()
    get_hit_sound = pygame.mixer.Sound("get_hit.wav")
    get_hit_sound.set_volume(0.2)
    collision_sound = pygame.mixer.Sound("collision.wav")
    collision_sound.set_volume(0.2)
    game_over_sound = pygame.mixer.Sound("game_over.mp3")
    game_over_sound.set_volume(0.2)

    # Hintergrundsound laden
    game_sound = pygame.mixer.Sound("game_sound.mp3")

    # Soundkanal erstellen
    background_channel = pygame.mixer.Channel(1)

    # Hintergrundsound auf dem Kanal abspielen (unendliche Wiederholung)
    background_channel.play(game_sound, loops=-1)

    # Lautstärke einstellen der Spielmusik
    game_sound.set_volume(0.1)

    # Variable für den Game Over Sound
    game_over_sound_played = False

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
                get_hit_sound.play()
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

                    collision_sound.play()

                    # Floating Text anzeigen und aktualisieren
                    #floating_text["position"] = [enemy[0], enemy[1]]
                    #floating_text["alpha"] = 255

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
                speed = 30
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
            if len(enemies) < 5 and anzahl <= 10:
                spawn_enemy()
                enemy_speed = 1
                enemy_size = 35
            if len(enemies) < 5 and anzahl <= 25:
                enemy_speed = 1.25
                enemy_size = 32
            if anzahl > 50:
                enemy_speed = 1.5
                enemy_size = 29
            if anzahl > 100:
                enemy_speed = 1.75
                enemy_size = 26
            if anzahl > 150:
                enemy_speed = 2
                enemy_size = 23
            if anzahl > 200:
                enemy_speed = 2.25
                enemy_size = 20
            if anzahl > 250:
                enemy_speed = 2.5
                enemy_size = 20
            if anzahl > 300:
                enemy_speed = 2.75
                enemy_size = 20
            if anzahl > 350:
                enemy_speed = 3
                enemy_size = 20
            if anzahl > 400:
                enemy_speed = 3.25
                enemy_size = 20
            if anzahl > 450:
                enemy_speed = 3.5
                enemy_size = 20
            if anzahl > 500:
                enemy_speed = 3.75
            if anzahl > 550:
                enemy_speed = 4
                enemy_size = 18

                # Gegner zeichnen und bewegen
            for enemy in enemies:
                pygame.draw.circle(screen, enemy_color, [int(enemy[0]), int(enemy[1])], enemy_size)

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

            # Floating Text anzeigen und aktualisieren
            if floating_text["alpha"] > 0:
                floating_text["alpha"] -= 5
                floating_text_surface = font.render(floating_text["text"], True,
                                                    (255, 255, 255, floating_text["alpha"]))
                screen.blit(floating_text_surface, (floating_text["position"][0], floating_text["position"][1]))


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
                                return False

                # Game Over Text
                screen.blit(game_over_text, game_over_rect)
                pygame.display.update()
                score_text = font.render("Score: " + str(score), True, WHITE)
                screen.blit(score_text, [870, 300])
                wiederholen_text = font.render("Mit Leertaste Spiel neustarten !", True, WHITE)
                screen.blit(wiederholen_text, [690, 950])



                if not game_over_sound_played:
                     game_over_sound.play()
                     game_over_sound_played = True

                background_channel.stop()

def run_game():
    while True:
        main_game()

#Aufruf der main_game() Funktion
run_game()
