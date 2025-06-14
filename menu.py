import stone_merge
import pygame
from pygame.locals import *

# window parameters
size = (500, 600)
BACKGROUND_COLOR = (142, 102, 83)
OUTLINE_COLOR = (118, 154, 181)

pygame.init()

screen = pygame.display.set_mode(size)

background = pygame.image.load('images/background_1.png')

# Load button images
play_button_image = pygame.image.load('images/button1.png')
rules_button_image = pygame.image.load('images/button3.png')
leaderboard_button_image = pygame.image.load('images/button2.png')
exit_button_image = pygame.image.load('images/button4.png')
easy_button_image = pygame.image.load('images/easy.png')
medium_button_image = pygame.image.load('images/medium.png')
hard_button_image = pygame.image.load('images/hard.png')
cross = pygame.image.load('images/cross.png')

running = True

custom_font_name = "Arial Rounded"
font_size = 30
rules_font_size = 26
font = pygame.font.SysFont(custom_font_name, font_size)
font_rules = pygame.font.SysFont(custom_font_name, rules_font_size)

# Menu button coordinates and sizes
menu_buttons = [
    {"image": play_button_image, "rect": pygame.Rect(120, 120, 250, 50)},
    {"image": rules_button_image, "rect": pygame.Rect(120, 220, 250, 50)},
    {"image": leaderboard_button_image, "rect": pygame.Rect(120, 320, 250, 50)},
    {"image": exit_button_image, "rect": pygame.Rect(120, 420, 250, 50)},
    {"image": easy_button_image, "rect": pygame.Rect(120, 150, 250, 50)},
    {"image": medium_button_image, "rect": pygame.Rect(120, 250, 250, 50)},
    {"image": hard_button_image, "rect": pygame.Rect(120, 350, 250, 50)},
    {"image": cross, "rect": pygame.Rect(400, 50, 50, 50)}
]

rules = False
play = False
leaderboard = False
game = 0

def get_scores(filename="scores.txt"):
    try:
        with open(filename, "r") as file:
            scores = [line.strip().split(",") for line in file]
            scores = [{"name": name, "score": int(score)} for name, score in scores]
    except FileNotFoundError:
        scores = []
    return scores

while running:
    screen.blit(background, (-400, 0))

    if rules:
        pygame.draw.rect(screen, OUTLINE_COLOR, (125, 50, 260, 50), border_radius=9)
        stone_merge.draw_text("READ THIS:", font, (255, 255, 255), 170, 60)

        pygame.draw.rect(screen, OUTLINE_COLOR, (50, 140, 400, 370), border_radius=9)
        stone_merge.draw_text("The main point of the game -", font_rules, (255, 255, 255), 70, 160)
        stone_merge.draw_text("combine the stones!", font_rules, (255, 255, 255), 70, 200)

        stone_merge.draw_text("The more stones you merge,", font_rules, (255, 255, 255), 70, 260)
        stone_merge.draw_text("then higher the score will be.", font_rules, (255, 255, 255), 70, 300)

        stone_merge.draw_text("Make it until you have", font_rules, (255, 255, 255), 70, 360)
        stone_merge.draw_text("run out of space!", font_rules, (255, 255, 255), 70, 400)

        stone_merge.draw_text("GOOD LUCK!", font_rules, (255, 255, 255), 170, 460)
        screen.blit(cross, (400, 50))

    elif leaderboard:
        screen.blit(cross, (400, 50))
        scores = get_scores()
        scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
        y_offset = 150

        pygame.draw.rect(screen, OUTLINE_COLOR, (100, 50, 280, 50), border_radius=9)
        stone_merge.draw_text("TOP PLAYERS:", font, (255, 255, 255), 130, 60)
        
        pygame.draw.rect(screen, OUTLINE_COLOR, (100, 140, 280, 330), border_radius=9)
        for i, record in enumerate(scores[:10], start=1):
            stone_merge.draw_text(f"{i}. {record['name']} — {record['score']}", font, (255, 255, 255), 110, y_offset)
            y_offset += 30

    elif play:
        if game == 0:
            for i in range(4, 7):
                screen.blit(menu_buttons[i]["image"], menu_buttons[i]["rect"].topleft)
            screen.blit(cross, (400, 50))
        else:
            if game == 1:
                difficulty = "Easy"
            elif game == 2:
                difficulty = "Medium"
            elif game == 3:
                difficulty = "Hard"
            
            stone_merge.play_game(difficulty)
            game = 0
            play = False
    else:
        for i in range(4):
            screen.blit(menu_buttons[i]["image"], menu_buttons[i]["rect"].topleft)
        
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN:
            if menu_buttons[0]["rect"].collidepoint(event.pos) and not play:
                play = True
                game = 0  # Reset game selection
            elif play and menu_buttons[4]["rect"].collidepoint(event.pos):
                game = 1
            elif play and menu_buttons[5]["rect"].collidepoint(event.pos):
                game = 2
            elif play and menu_buttons[6]["rect"].collidepoint(event.pos):
                game = 3
            elif menu_buttons[1]["rect"].collidepoint(event.pos) and not play and not leaderboard:
                rules = True
            elif menu_buttons[2]["rect"].collidepoint(event.pos) and not play and not rules:
                leaderboard = True
            elif menu_buttons[3]["rect"].collidepoint(event.pos) and not play and not rules and not leaderboard:
                running = False
            elif menu_buttons[7]["rect"].collidepoint(event.pos) and (play or rules or leaderboard):
                play = False
                rules = False
                leaderboard = False

pygame.quit()
