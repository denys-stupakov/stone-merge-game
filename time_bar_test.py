import pygame
import time

border = 100
size = (500, 600)

pygame.init()

screen = pygame.display.set_mode(size)
OUTLINE_COLOR = (118, 154, 181)
OUTLINE_THICKNESS = 5
BACKGROUND_COLOR = (137, 180, 212)

running = True

import pygame
import time

border = 100
size = (500, 600)

pygame.init()

screen = pygame.display.set_mode(size)
OUTLINE_COLOR = (118, 154, 181)
OUTLINE_THICKNESS = 5
BACKGROUND_COLOR = (137, 180, 212)

running = True

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

time_bar = Time_bar("Hard")
time_bar.draw_bar()

start_time = time.time()

while running:
    screen.fill(BACKGROUND_COLOR)
    time_bar.draw_bar()
    end_time = time.time()
    time_bar.update_bar(start_time, end_time, 0)
    time_bar.check_bars()

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()