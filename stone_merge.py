import random
import time

import pygame
from pygame.locals import *

# parameters
size = (500, 600)
width, height = 300, 400
ROWS = 8
COLS = 6
rect_w = 50
border = 100
rect_h = 50

score = 0

pygame.init()
running = True
screen = pygame.display.set_mode(size)
pygame.display.set_caption("StoneMerge")
OUTLINE_COLOR = (118, 154, 181)
OUTLINE_THICKNESS = 5
BACKGROUND_COLOR = (137, 180, 212)

# Background Sound
pygame.mixer.music.load("music_1.wav")
pygame.mixer.music.play(-1)

# Load buttons images
img_resume = pygame.image.load('images/continue.png') 
img_save_and_exit = pygame.image.load('images/exit.png') 
img_music = pygame.image.load('images/unmute.png') 
img_restart = pygame.image.load('images/restart.png')

# Menu buttons coordinates and sizes
pause_buttons = [
    {"image": img_resume, "rect": pygame.Rect(145, 270, 48, 48)},
    {"image": img_restart, "rect": pygame.Rect(204, 270, 48, 48)},
    {"image": img_music, "rect": pygame.Rect(263, 270, 48, 48)},
    {"image": img_save_and_exit, "rect": pygame.Rect(322, 270, 48, 48)}
]


custom_font_name = "Arial Rounded"
font_size = 30
font = pygame.font.SysFont(custom_font_name, font_size)

def draw_text(text, font, text_color, x, y):
    text = font.render(text, True, text_color)
    screen.blit(text, (x, y))

#FUNCTIONS FOR RECORDS
def save_score(name, score, filename="scores.txt"):
    try:
        with open(filename, "r") as file:
            scores = [line.strip().split(",") for line in file]
            scores_dict = {name: int(score) for name, score in scores}
    except FileNotFoundError:
        scores_dict = {}

    if name in scores_dict:
        if score > scores_dict[name]:
            scores_dict[name] = score
    else:
        scores_dict[name] = score

    sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)[:10]

    with open(filename, "w") as file:
        for name, score in sorted_scores:
            file.write(f"{name},{score}\n")



def print_top_3(filename="scores.txt"):
    try:
        with open(filename, "r") as file:
            scores = [line.strip().split(",") for line in file]
            scores = [{"name": name, "score": int(score)} for name, score in scores]
    except FileNotFoundError:
        scores = []

    print("Top 3 Players:")
    for i, record in enumerate(scores[:3], start=1):
        print(f"{i}. {record['name']} - {record['score']}")



def clear_scores(filename="scores.txt"):
    with open(filename, "w") as file:
        file.write("")


# grid positions
grid_pos = [
    (border + idx * rect_w, border + idy * rect_h)
    for idy in range(ROWS)
    for idx in range(COLS)
]

def draw_grid(screen):
    for row in range(1, ROWS):
        y = border + row * rect_h
        pygame.draw.line(
            screen,
            OUTLINE_COLOR,
            (border, y),
            (width + border - 5, y),
            OUTLINE_THICKNESS,
        )

    for col in range(1, COLS):
        x = border + col * rect_w
        pygame.draw.line(screen, OUTLINE_COLOR, (x, border), (x, height + border - 5), OUTLINE_THICKNESS)

    pygame.draw.rect(screen, OUTLINE_COLOR, (border, border, width, height), OUTLINE_THICKNESS)


def merge(tiles, selected_tile):
    global score
    merged_tiles = []
    merged = False
    spot_is_taken = False

    for tile in tiles:
        if (
            tile.value == selected_tile.value
            and tile.tag != selected_tile.tag
            and tile.x == selected_tile.x
            and tile.y == selected_tile.y
        ):
            merged = True
            # Do not add the merged tiles to the new list
        elif (
            tile.value != selected_tile.value
            and tile.tag != selected_tile.tag
            and tile.x == selected_tile.x
            and tile.y == selected_tile.y
        ):
            spot_is_taken = True
            # Add a tile to the new list nut position remains
            merged_tiles.append(tile)
        else:
            merged_tiles.append(tile)

    if spot_is_taken:
        selected_tile.x = initial_point[0]
        selected_tile.y = initial_point[1]
        return merged_tiles

    if merged:
        if selected_tile in merged_tiles:
            merged_tiles.remove(selected_tile)
        tag = generating_tag(tiles)
        new_tile = Tile(tag, selected_tile.value + 1, pygame.image.load(f"images/tile{selected_tile.value + 1}.png"), selected_tile.row, selected_tile.col)
        merged_tiles.append(new_tile)
        score += new_tile.value
    return merged_tiles


def rand_row(tiles):
    max_value = 0
    # finds maximum value
    for tile in tiles:
        if tile.value > max_value:
            max_value = tile.value

    for tile in tiles:
        # gameover
        if tile.row == 0:
            return True
        tile.row -= 1
        tile.y = border + tile.row * rect_h

    for i in range(COLS):
        if max_value == 0:
            value = int(random.randrange(1, 4))
        else:
            value = int(random.randrange(1, max_value + 1))
        tag = generating_tag(tiles)
        tiles.append(Tile(tag, value, pygame.image.load(f"images/tile{value}.png"), ROWS - 1, i))

    return False

def generating_tag(tiles):
    tags = [tile.tag for tile in tiles]
    tags.sort()
    #generating first time:
    if len(tags) == 0:
        return 1
    
    for i in range(1, len(tags) + 1):
        if i not in tags:
            return i

    return max(tags) + 1

# DRAWING SCORE
def draw_score(screen, score, text_color = (65, 80, 125)):
    text = font.render(f"Score: {score}", True, text_color)
    screen.blit(text, (160, 520))
    pygame.draw.rect(screen, OUTLINE_COLOR, (148, 513, 205, 48), OUTLINE_THICKNESS)

# CLASS TILE
class Tile:
    def __init__(self, tag, value, img, row, col):
        self.tag = tag
        self.value = value
        self.tile = img
        self.row = row
        self.col = col
        self.x = border + col * rect_w
        self.y = border + row * rect_h
        self.picked = False

    def draw(self, screen):
        screen.blit(self.tile, self.tile.get_rect(center = (self.x + rect_w / 2, self.y + rect_h / 2)))

    def snap_to_grid(self):
        # Find the closest grid position
        min_distance = float("inf")
        closest_pos = None
        for pos in grid_pos:
            distance = ((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_pos = pos
        self.x, self.y = closest_pos
        self.row = int((self.y - border) / rect_h)
        self.col = int((self.x - border) / rect_w)

    def land(self, start_time, paused_time, time_bar):
        tiles_landing_speed = 0.7
        acceleration = 0.01
        if self.row == ROWS - 1:
            return
        for tile in tiles:
            if tile.col == self.col and tile.row == self.row + 1:
                if (
                    tile.value == self.value
                    and self.value != 15
                    and self.picked
                    and (self.x != initial_point[0] or self.y != initial_point[1])
                ):
                    self.row += 1
                    self.y = border + self.row * rect_h
                return
        tiles.sort(key = lambda x: x.y)
        for tile in tiles:
            if tile.col == self.col and tile.row > self.row:
                while self.y < tile.row * rect_h + border - rect_h:
                    self.y += tiles_landing_speed
                    tiles_landing_speed += acceleration
                    self.row = int((self.y - border) / rect_h)

                    #draws game objects on screen
                    screen.fill(BACKGROUND_COLOR)
                    draw_grid(screen)
                    end_time = time.time()
                    time_bar.draw_bar()
                    time_bar.update_bar(start_time, end_time, paused_time)
                    draw_score(screen, score, (65, 80, 125))
                    screen.blit(pause_icon, (425, 35))
                    for t in tiles:
                        t.draw(screen)
                    pygame.display.update()

                self.snap_to_grid()
                pygame.display.update()
                if self.value != 15 and tile.value == self.value and self.picked:
                    self.row = tile.row
                    self.y = border + self.row * rect_h
                return
        self.row = ROWS - 1
        self.y = border + self.row * rect_h

def diagonal_move(tiles, selected_tile):
    min_distance = float("inf")
    closest_pos = None
    for pos in grid_pos:
        distance = ((selected_tile.x - pos[0]) ** 2 + (selected_tile.y - pos[1]) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_pos = pos
    row = int((closest_pos[1] - border) / rect_h)
    col = int((closest_pos[0] - border) / rect_w)
    for tile in tiles:
        if tile.row == row and tile.col == col and tile.tag != selected_tile.tag and (tile.value != selected_tile.value or selected_tile.value == 15):
            if abs(abs(selected_tile.x-initial_point[0])-abs(selected_tile.y-initial_point[1])) > 5 or selected_tile.value == 15:
                return False
    return True

class Time_bar:
    def __init__(self, difficulty):
        if difficulty == "Easy":
            self.time_for_bar = 1
        elif difficulty == "Medium":
            self.time_for_bar = 0.75
        else:
            self.time_for_bar = 0.5

        self.generated_rows = 0    

        self.x = 1.25 * border
        self.y = border / 4
        self.width = size[0] - 1.25 * border - self.x
        self.height = self.y * 3 - border / 20

        padding = (border / 2) / 11
        width_for_blocks = (self.width - padding * 11) / 10
        
        #color for blocks
        self.color = (65, 85, 125)

        # self.blocks[][0] - start_x, self.blocks[][1] - start_y, self.blocks[][2] - width, self.blocks[][3] - height, self.blocks[][4] - full
        self.blocks = []
        for i in range(
            int(self.x) + int(padding),
            int(self.width + self.x) - 20,
            int(padding + width_for_blocks),
        ):
            self.blocks.append([i + padding, self.y + border / 10, width_for_blocks, self.height - border / 5, False])

    def draw_bar(self):
        pygame.draw.rect(screen, OUTLINE_COLOR, (self.x, self.y, self.width + 2.5, self.height), OUTLINE_THICKNESS)
        for block in self.blocks:
            pygame.draw.rect(screen, OUTLINE_COLOR, (block[0], block[1], block[2], block[3]), width = 1)

    def update_bar(self, start_time, current_time, paused_time):
        elapsed_time = current_time - start_time - paused_time

        for i in range(10):
            bar_time = elapsed_time - (i + self.generated_rows * 10) * self.time_for_bar
            if bar_time >= self.time_for_bar:
                self.blocks[i][4] = True
                pygame.draw.rect(screen, self.color, (self.blocks[i][0], self.blocks[i][1], self.blocks[i][2], self.blocks[i][3]))
            elif bar_time > 0:
                height_for_bar = self.blocks[i][3] * (bar_time / self.time_for_bar)
                pygame.draw.rect(screen, self.color, (self.blocks[i][0], self.blocks[i][1] + self.blocks[i][3] - height_for_bar, self.blocks[i][2], height_for_bar))

    def nullify(self):
        for block in self.blocks:
            block[4] = False

    def check_bars(self):
        for i in range(10):
            if self.blocks[i][4] == False:
                return False

        self.nullify()
        self.generated_rows += 1
        return True

# all dependencies
tiles = []

#flags
selected_tile = None
IsBlocked = False
dragging = False
clock = pygame.time.Clock()
initial = True
initial_point = []
paused_pos = None
paused_mus = False

pause_icon = pygame.image.load("images/pause.png")
pause_icon = pygame.transform.scale(pause_icon, (50, 50))

dim_surface = pygame.Surface(size, pygame.SRCALPHA)
dim_surface.fill((0, 0, 0, 150))

# MAIN LOOP
def play_game(difficulty):
    global tiles, selected_tile, IsBlocked, dragging, initial, initial_point, score, paused_pos, paused_mus
    selected_tile = None

    time_bar = Time_bar(difficulty)
    paused_time = 0

    running = True
    pause = False
    gameover = False
    
    rand_row(tiles)
    rand_row(tiles)
    rand_row(tiles)

    #For saving players' names
    name = ""
    entering_name = True
    name = ""

    #For closing name-entering menu
    name_rect = pygame.Rect(60, 200, 380, 50)
    cross = pygame.image.load('images/cross.png')
    cross_rect = cross.get_rect(topleft=(400, 50))

    while running:
        #If in name-entering mode
        if entering_name:
            screen.fill(BACKGROUND_COLOR)
            pygame.draw.rect(screen, (87, 114, 161), (40, 130, 420, 160), border_radius = 10)
            pygame.draw.rect(screen, BACKGROUND_COLOR, name_rect, border_radius = 10)
            screen.blit(cross, (400, 50))
            draw_text("Enter your name:", font, (255, 255, 255), 130, 150)
            draw_text(name, font, (255, 255, 255), name_rect.x + 10, name_rect.y + 10)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    tiles.clear()
                    paused_time = 0
                    score = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if cross_rect.collidepoint(event.pos):
                        entering_name = False
                        running = False
                        tiles.clear()
                        paused_time = 0
                        score = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        entering_name = False
                        start_time = time.time()
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 15:
                            name += event.unicode
        #Other checks
        else:
            if pause == True:
                screen.fill(BACKGROUND_COLOR)
                draw_grid(screen)
                for tile in tiles:
                    tile.draw(screen)
                time_bar.draw_bar()
                time_bar.update_bar(start_time, end_time, paused_time)
                screen.blit(dim_surface, (0,0))

                pygame.draw.rect(screen, OUTLINE_COLOR, (60, 180, 380, 200), border_radius = 40)
                for i in range(0, 4):
                    screen.blit(pause_buttons[i]["image"], pause_buttons[i]["rect"].topleft)
                draw_text("Pause", font, (255, 255, 255), 210, 200)

                for event in pygame.event.get():
                        if event.type == QUIT:
                            tiles.clear()
                            score = 0
                            running = False
                            break
                        
                        elif event.type == MOUSEBUTTONDOWN:
                            #resume
                            if pygame.Rect(140, 270, 48, 48).collidepoint(event.pos):
                                pause = False
                                end_pause_time = time.time()
                                paused_time += end_pause_time - start_pause_time
                            #exit    
                            elif pygame.Rect(327, 270, 48, 48).collidepoint(event.pos):
                                tiles.clear()
                                score = 0
                                running = False
                                break
                            #music
                            elif pygame.Rect(258, 270, 48, 48).collidepoint(event.pos):
                                if paused_mus:
                                    pygame.mixer.music.play(start = paused_pos / 1000.0)
                                    img_music = pygame.image.load('images/unmute.png')
                                    pause_buttons[2]["image"] = img_music
        
                                    paused_mus = False
                                elif not paused_mus:
                                    paused_pos = pygame.mixer.music.get_pos()
                                    pygame.mixer.music.stop()
                                    img_music = pygame.image.load('images/mute.png')
                                    pause_buttons[2]["image"] = img_music
                                    paused_mus = True
                            #game restart
                            elif pygame.Rect(199, 270, 48, 48).collidepoint(event.pos):
                                tiles.clear()
                                rand_row(tiles)
                                rand_row(tiles)
                                rand_row(tiles)
                                score = 0
                                running = True

                                time_bar = Time_bar(difficulty)
                                start_time = time.time()
                                pause = False
                                paused_time = 0
                                continue
                pygame.display.update()
            elif gameover:
                for event in pygame.event.get():                
                    if event.type == QUIT:
                        tiles.clear()
                        running = False
                        score = 0
                        break
                    
                    elif event.type == MOUSEBUTTONDOWN:
                        if pygame.Rect(100, 100, 300, 200).collidepoint(event.pos):
                            running = False
                            break
            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        tiles.clear()
                        score = 0
                        running = False
                        break

                    elif event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                        #pause check
                            if pygame.Rect(425, 35, 50, 50).collidepoint(event.pos):
                                pause = True
                                start_pause_time = time.time()
                                break

                            #check for tiles
                            else:
                                for tile in tiles:
                                    tile_rect = tile.tile.get_rect(center=(tile.x + rect_w / 2, tile.y + rect_h / 2))
                                    if tile_rect.collidepoint(event.pos):
                                        dragging = True
                                        IsBlocked = False
                                        if initial:
                                            initial_point = tile.x, tile.y
                                            initial = False
                                        selected_tile = tile
                                        # Calculate offset to maintain relative position between mouse and tile center
                                        offset_x = tile.x - event.pos[0]
                                        offset_y = tile.y - event.pos[1]
                    elif event.type == MOUSEBUTTONUP:
                        dragging = False
                        if selected_tile != None:
                            selected_tile.picked = True
                        initial = True
                        if event.button == 1:
                            if selected_tile != None:
                                selected_tile.snap_to_grid()
                                if selected_tile.value == 15:
                                    for tile in tiles:
                                        if tile.row == selected_tile.row and tile.col == selected_tile.col and tile.tag != selected_tile.tag:
                                            selected_tile.x, selected_tile.y = initial_point
                                            selected_tile.snap_to_grid()
                                for tile in tiles:
                                    if (
                                        tile.row == selected_tile.row
                                        and tile.col == selected_tile.col
                                        and tile.tag != selected_tile.tag
                                    ):
                                        selected_tile.x = initial_point[0]
                                        selected_tile.y = initial_point[1]
                                        selected_tile.snap_to_grid()
                                        selected_tile = None
                                        break
                    elif event.type == MOUSEMOTION:
                        if dragging and not IsBlocked:
                            selected_tile.x = event.pos[0] + offset_x
                            selected_tile.y = event.pos[1] + offset_y
                            for tile in tiles:
                                tile_rect = tile.tile.get_rect(center = (tile.x + rect_w / 2, tile.y + rect_h / 2))
                                if (
                                    (
                                        not diagonal_move(tiles, selected_tile)
                                    )
                                    or event.pos[0] < 100
                                    or event.pos[0] > 380
                                    or event.pos[1] > 480
                                    or event.pos[1] < 110
                                ):
                                    selected_tile.x = initial_point[0]
                                    selected_tile.y = initial_point[1]
                                    selected_tile.snap_to_grid()
                                    dragging = False
                                    IsBlocked = True

                                elif (
                                    tile_rect.collidepoint(event.pos)
                                    and tile.tag != selected_tile.tag
                                    and tile.value != selected_tile.value
                                ):
                                    selected_tile.x = initial_point[0]
                                    selected_tile.y = initial_point[1]
                                    selected_tile.snap_to_grid()
                                    dragging = False
                                    IsBlocked = True

                                elif (
                                    (
                                        tile_rect.collidepoint(event.pos)
                                        or tile_rect.collidepoint([event.pos[0] + 10, event.pos[1] + 10])
                                        or tile_rect.collidepoint([event.pos[0] - 10, event.pos[1] - 10])
                                    )
                                    and tile.tag != selected_tile.tag
                                    and tile.value == selected_tile.value
                                    and tile.value != 15
                                ):
                                    selected_tile.x = tile.x
                                    selected_tile.y = tile.y
                                    selected_tile.snap_to_grid()
                                    tiles = merge(tiles, selected_tile)
                                    dragging = False
                if not pause:
                    screen.fill(BACKGROUND_COLOR)
                    screen.blit(pause_icon, (425, 35))
                    draw_grid(screen)
                    time_bar.draw_bar()
                    end_time = time.time()
                    time_bar.update_bar(start_time, end_time, paused_time)

                    if time_bar.check_bars():
                        if dragging:
                            selected_tile.x = initial_point[0]
                            selected_tile.y = initial_point[1]
                            selected_tile.snap_to_grid()
                            dragging = False
                            selected_tile = None
                        #gameover
                        if rand_row(tiles):
                            gameover = True
                            tile.land(start_time, paused_time, time_bar)
                            for t in tiles:
                                t.draw(screen)
                            tiles.clear()            
                            screen.blit(dim_surface, (0, 0))
                            pygame.draw.rect(screen, OUTLINE_COLOR, (100, 150, 300, 200), border_radius = 40)
                            draw_text("GAMEOVER!", font, (255, 255, 255), 160, 230)            
                            pygame.display.update()
                            save_score(name, score)
                            score = 0
                            continue

                    for tile in tiles:
                        tile.land(start_time, paused_time, time_bar)
                        tile.picked = False
                        tiles = merge(tiles, tile)
                        tile.draw(screen)

                    draw_score(screen, score, (65, 80, 125))
                    pygame.display.update()
            clock.tick(144)