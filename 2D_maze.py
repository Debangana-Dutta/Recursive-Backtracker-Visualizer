import pygame
import random
import time

cellSize = 40
mazeWidth = 15
mazeHeight = 10 
screenWidth = mazeWidth * cellSize
screenHeight = mazeHeight * cellSize + 50



# colour palette
BLUE_BG = (15, 15, 25)  # deep charcoal background screen
WALL = (255, 215, 0)  # wall colour=gold
GREEN = (102, 255, 102)  # starting cell bg colour
PURPLE = (150, 0, 200)  # ending cell bg colour
ORANGE = (255, 150, 0)  # player colour
PINK = (255, 99, 171)  # 'regenerate maze' text colour
WHITE = (255, 255, 255)  # using it for end position cell colour text, etc
lineWidth = 2
buttonWidth = 250
buttonHeight = 35

# Maze class
class MazeGame:
    def __init__(self, w, h):
        self.mazeWidth = w
        self.mazeHeight = h
        self.start = (0, 0)
        self.end = (w - 1, h - 1)
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption("2D Maze Solver Game")
        self.font_small = pygame.font.Font(None, 28)  # small font is used for texts like regenerate maze
        self.font_label = pygame.font.Font(None, 18)  # label font which is used for Start and End text sizee
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_down = False
        self.won = False
        self.status = ""
        self.generate_maze()

    def generate_maze(self):
        # Generates a maze using Recursive Backtracker
        # Grid setup:[Top, Right, Bottom, Left] and walls are True by default
        self.grid = [[{'walls': [True] * 4, 'visited': False}
                      for i in range(self.mazeWidth)] for j in range(self.mazeHeight)]
        self.won = False
        self.status = ""
        self.player = self.start

        stack = [self.start]
        cx, cy = self.start
        self.grid[cy][cx]['visited'] = True

        while stack:
            unvisited_neighbors = []
            for (nx, ny), wall_index in self.get_neighbors(cx, cy):
                if not self.grid[ny][nx]['visited']:
                    opposite_wall = (wall_index + 2) % 4
                    unvisited_neighbors.append(((nx, ny), wall_index, opposite_wall))
            if unvisited_neighbors:
                (nx, ny), current_wall, neighbor_wall = random.choice(unvisited_neighbors)
                #breaking the wall
                self.grid[cy][cx]['walls'][current_wall] = False
                self.grid[ny][nx]['walls'][neighbor_wall] = False
                stack.append((nx, ny))
                cx, cy = nx, ny
                self.grid[cy][cx]['visited'] = True
            else:
                stack.pop()
                if stack:
                    cx, cy = stack[-1]

    def get_neighbors(self, x, y):
        # returns valid neighbors and the wall index connecting them
        neighbors = []
        # (dx, dy, current_cell_wall_index)
        for dx, dy, wall in [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.mazeWidth and 0 <= ny < self.mazeHeight:  # Used self.mazeWidth/self.mazeHeight
                neighbors.append(((nx, ny), wall))
        return neighbors

    def rectangle(self, pos, color):
        #drwaing a solid colored square for the cell
        x, y = pos
        pygame.draw.rect(self.screen, color,
                         (x * cellSize + 2, y * cellSize + 2,  
                          cellSize - 4, cellSize - 4))  

    def label(self, pos, text, color):
        """Center text label on a cell"""
        x, y = pos
        center_x = x * cellSize + cellSize // 2  
        center_y = y * cellSize + cellSize // 2  
        text_surf = self.font_label.render(text, True, color)
        text_rect = text_surf.get_rect(center=(center_x, center_y))
        self.screen.blit(text_surf, text_rect)

    def get_button_rect(self):
        """Calculate and return the Rectangle for regenerate button."""
        return pygame.Rect((screenWidth - buttonWidth) // 2, screenHeight - 40,  
                           buttonWidth, buttonHeight)  

    def draw(self):
        """Show the entire game screen"""
        self.screen.fill(BLUE_BG)
        # Maze walls
        for y in range(self.mazeHeight):  #used self.mazeHeight
            for x in range(self.mazeWidth):  #used self.mazeWidth
                rect_x, rect_y = x * cellSize, y * cellSize  #used cellSize
                walls = self.grid[y][x]['walls']

                # Wall 0: Top, 1: Right, 2: Bottom, 3: Left
                if walls[0]: pygame.draw.line(self.screen, WALL, (rect_x, rect_y), (rect_x + cellSize, rect_y),
                                              lineWidth)
                if walls[1]: pygame.draw.line(self.screen, WALL, (rect_x + cellSize, rect_y),
                                              (rect_x + cellSize, rect_y + cellSize),
                                              lineWidth)
                if walls[2]: pygame.draw.line(self.screen, WALL, (rect_x, rect_y + cellSize),
                                              (rect_x + cellSize, rect_y + cellSize),
                                              lineWidth)
                if walls[3]: pygame.draw.line(self.screen, WALL, (rect_x, rect_y), (rect_x, rect_y + cellSize),
                                              lineWidth)
        # Start and end background colors
        self.rectangle(self.start, GREEN)
        self.rectangle(self.end, PURPLE)

        # Player
        if not self.won:
            px, py = self.player
            center_x = px * cellSize + cellSize // 2  #udesd cellSize
            center_y = py * cellSize + cellSize // 2  #used cellSize
            pygame.draw.circle(self.screen, ORANGE, (center_x, center_y), cellSize // 3)  # Used cellSize
        # Labels
        self.label(self.start, "START", BLUE_BG)
        self.label(self.end, "END", WHITE)
        # Regenerate Button
        reg_maze = self.get_button_rect()
        pygame.draw.rect(self.screen, PINK, reg_maze, border_radius=8)
        regen_text_surf = self.font_small.render("REGENERATE MAZE", True, BLUE_BG)
        regen_text_rect = regen_text_surf.get_rect(center=reg_maze.center)
        self.screen.blit(regen_text_surf, regen_text_rect)

        # Status Text
        gameStatus = self.font_small.render(self.status, True, WHITE)
        self.screen.blit(gameStatus, (screenWidth - gameStatus.get_width() - 10,
                                      screenHeight - 35))  # Used screenWidth/screenHeight

        # Victory
        if self.won:
            overlay = pygame.Surface(
                (screenWidth, self.mazeHeight * cellSize))  # Used screenWidth/self.mazeHeight/cellSize
            overlay.set_alpha(220)
            overlay.fill(BLUE_BG)
            self.screen.blit(overlay, (0, 0))

            f_congrats = pygame.font.Font(None, 80)
            congrats_surf = f_congrats.render("CONGRATULATIONS!", True, PINK)
            final_message = self.font_label.render("You have successfully completed the maze!", True, WHITE)

            congrats_rect = congrats_surf.get_rect(
                center=(screenWidth // 2, screenHeight // 2 - 45))  # Used screenWidth/screenHeight
            message_rect = final_message.get_rect(
                center=(screenWidth // 2, screenHeight // 2 + 5))  # Used screenWidth/screenHeight

            self.screen.blit(congrats_surf, congrats_rect)
            self.screen.blit(final_message, message_rect)

        pygame.display.flip()

    def movePlayer(self, target_pos):
        # Attempts movement if adjacent and the wall is open
        px, py = self.player
        tx, ty = target_pos

        is_adjacent = abs(tx - px) + abs(ty - py) == 1

        if is_adjacent and self.player != self.end:
            dx, dy = tx - px, ty - py
            # Determine wall index (0: Up, 1: Right, 2: Down, 3: Left)
            wall_index = -1
            if dx == 1:
                wall_index = 1
            elif dx == -1:
                wall_index = 3
            elif dy == 1:
                wall_index = 2
            elif dy == -1:
                wall_index = 0
            #checking if the path is open (wall is False)
            if wall_index != -1 and not self.grid[py][px]['walls'][wall_index]:
                self.player = target_pos
                #checking for win condition
                if self.player == self.end:
                    self.won = True
                    self.status = "VICTORY!"
                return True
        return False

    def run(self):
        #main game loop, handling events
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                #hanlindg clicks and button interactions
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.is_down = True
                    mouse_x, mouse_y = event.pos

                    if self.get_button_rect().collidepoint(mouse_x, mouse_y):
                        self.generate_maze()

                    #singleclick movement (if in maze area and not won)
                    elif mouse_y < self.mazeHeight * cellSize and not self.won:  # Used self.mazeHeight/cellSize
                        target_pos = (mouse_x // cellSize, mouse_y // cellSize)  # Used cellSize
                        self.movePlayer(target_pos)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.is_down = False
                #hanlding continuous dragging movement
                if event.type == pygame.MOUSEMOTION and self.is_down and not self.won:
                    mouse_x, mouse_y = event.pos
                    if mouse_y < self.mazeHeight * cellSize:  # Used self.mazeHeight/cellSize
                        target_pos = (mouse_x // cellSize, mouse_y // cellSize)  # Used cellSize
                        self.movePlayer(target_pos)
            self.draw()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = MazeGame(mazeWidth, mazeHeight)
    game.run()